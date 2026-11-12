import json
import os
import time
from json import JSONDecodeError

from dotenv import load_dotenv
from openai import (
    APIConnectionError,
    APIError,
    APIStatusError,
    APITimeoutError,
    OpenAI,
    RateLimitError,
)
from pydantic import BaseModel, ConfigDict, ValidationError
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

# Load local environment variables before importing the database engine.
load_dotenv()

from src.database import engine


# Groq uses an OpenAI-compatible API endpoint.
GROQ_MODEL = "openai/gpt-oss-20b"
GROQ_BASE_URL = "https://api.groq.com/openai/v1"
MAX_RETRIES = 3
REQUEST_TIMEOUT_SECONDS = 30

# Groq GPT-OSS 20B rates (USD per 1 million tokens); verify before future releases.
INPUT_PRICE_PER_MILLION = 0.075
CACHED_INPUT_PRICE_PER_MILLION = 0.0375
OUTPUT_PRICE_PER_MILLION = 0.30


class BusinessInsight(BaseModel):
    """The required structure for every AI-generated business insight."""

    model_config = ConfigDict(extra="forbid")

    summary: str
    key_points: list[str]
    recommendation: str


BASE_PROMPT = """
You are an e-commerce business analytics assistant.

Use only the verified data provided to you.

Rules:
- Do not invent, change, or guess numbers.
- Do not guess causes or reasons.
- Do not make claims that the data cannot prove.
- Do not perform new calculations.
- Do not combine multiple values to create a new metric.
- Treat the provided result as verified data.
- If the requested information is not available, say:
  "This information is not available in the available data."
- Do not discuss profit unless profit data is provided.
- Use simple English and short, clear sentences.
- Answer only what is asked.
- Return a concise summary, factual key points, and one practical recommendation.
- Every key point and recommendation must be supported by the verified result.
- Do not invent a business action that depends on information not provided.
"""


def _create_groq_client():
    """Create the Groq client without exposing the API key."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is missing. Add it to your local .env file."
        )

    return OpenAI(
        api_key=api_key,
        base_url=GROQ_BASE_URL,
        timeout=REQUEST_TIMEOUT_SECONDS,
        max_retries=0,  # Retries are handled explicitly below.
    )


def _retry_delay(error, attempt):
    """Use retry-after when supplied; otherwise use exponential backoff."""
    response = getattr(error, "response", None)
    headers = getattr(response, "headers", {}) or {}
    retry_after = headers.get("retry-after") or headers.get("Retry-After")

    if retry_after:
        try:
            return max(0.0, float(retry_after))
        except (TypeError, ValueError):
            pass

    return min(2 ** (attempt - 1), 8)


def _calculate_token_cost(usage):
    """Calculate estimated API cost from the usage returned by Groq."""
    input_tokens = int(getattr(usage, "prompt_tokens", 0) or 0)
    output_tokens = int(getattr(usage, "completion_tokens", 0) or 0)
    total_tokens = int(getattr(usage, "total_tokens", input_tokens + output_tokens) or 0)

    prompt_details = getattr(usage, "prompt_tokens_details", None)
    cached_input_tokens = int(
        getattr(prompt_details, "cached_tokens", 0) or 0
    )
    cached_input_tokens = min(cached_input_tokens, input_tokens)
    uncached_input_tokens = input_tokens - cached_input_tokens

    input_cost = (
        uncached_input_tokens * INPUT_PRICE_PER_MILLION
        + cached_input_tokens * CACHED_INPUT_PRICE_PER_MILLION
    ) / 1_000_000
    output_cost = output_tokens * OUTPUT_PRICE_PER_MILLION / 1_000_000

    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
        "cached_input_tokens": cached_input_tokens,
        "input_cost_usd": input_cost,
        "output_cost_usd": output_cost,
        "total_cost_usd": input_cost + output_cost,
        "pricing_note": "Estimated using the configured Groq GPT-OSS 20B rates; actual billing may vary.",
    }


def ask_llm(prompt):
    """Call Groq, validate its structured response, and return insight + usage."""
    client = _create_groq_client()
    last_error = None

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": BASE_PROMPT,
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "business_insight",
                        "strict": True,
                        "schema": BusinessInsight.model_json_schema(),
                    },
                },
                temperature=0.2,
                max_completion_tokens=500,
            )

            if not response.choices:
                raise ValueError("Groq returned no response choices.")

            choice = response.choices[0]
            message = choice.message

            if getattr(message, "refusal", None):
                raise ValueError(f"Groq refused the request: {message.refusal}")

            content = message.content
            if not content or not content.strip():
                raise ValueError("Groq returned an empty response.")

            # Parse JSON explicitly, then validate its fields and data types.
            parsed_json = json.loads(content)
            insight = BusinessInsight.model_validate(parsed_json)
            usage_data = _calculate_token_cost(response.usage) if response.usage else None

            return insight, usage_data

        except (RateLimitError, APITimeoutError, APIConnectionError, APIStatusError) as error:
            last_error = error
            status_code = getattr(error, "status_code", None)
            retryable = (
                isinstance(error, (RateLimitError, APITimeoutError, APIConnectionError))
                or (isinstance(error, APIStatusError) and status_code is not None and status_code >= 500)
            )

            if not retryable or attempt == MAX_RETRIES:
                break

            time.sleep(_retry_delay(error, attempt))

        except (JSONDecodeError, ValidationError, ValueError) as error:
            # Invalid model output is not blindly retried; report it clearly.
            raise RuntimeError(f"Groq returned an unusable response: {error}") from error

        except APIError as error:
            raise RuntimeError(f"Groq API request failed: {error}") from error

    if isinstance(last_error, RateLimitError):
        raise RuntimeError("Groq rate limit reached after the retry attempts. Please try again later.") from last_error
    if isinstance(last_error, APITimeoutError):
        raise RuntimeError("Groq request timed out after the retry attempts.") from last_error
    if isinstance(last_error, APIConnectionError):
        raise RuntimeError("Could not connect to Groq after the retry attempts. Check your internet connection.") from last_error
    if isinstance(last_error, APIStatusError):
        raise RuntimeError(
            f"Groq API returned an error (HTTP {last_error.status_code}) after the retry attempts."
        ) from last_error
    if last_error:
        raise RuntimeError(f"Groq request failed: {last_error}") from last_error
    raise RuntimeError("Groq request failed for an unknown reason.")


# --------------------------------------------------
# ALL SUPPORTED BUSINESS QUESTIONS
# --------------------------------------------------

questions = {

    "total_revenue": {
        "keywords": ["total", "revenue"],
        "query": text("""
            SELECT
                SUM(oi.price) AS total_revenue
            FROM orders o
            JOIN order_items oi
                ON o.order_id = oi.order_id;
        """)
    },

    "total_orders": {
        "keywords": ["total", "orders"],
        "query": text("""
            SELECT
                COUNT(DISTINCT order_id) AS total_orders
            FROM orders;
        """)
    },

    "total_customers": {
        "keywords": ["total", "customers"],
        "query": text("""
            SELECT
                COUNT(DISTINCT customer_unique_id) AS total_customers
            FROM customers;
        """)
    },

    "average_order_value": {
        "keywords": ["average", "order", "value"],
        "query": text("""
            SELECT
                SUM(oi.price) / COUNT(DISTINCT o.order_id)
                AS average_order_value
            FROM orders o
            JOIN order_items oi
                ON o.order_id = oi.order_id;
        """)
    },

    "total_freight": {
        "keywords": ["total", "freight"],
        "query": text("""
            SELECT
                SUM(freight_value) AS total_freight
            FROM order_items;
        """)
    },

    "total_products": {
        "keywords": ["total", "products"],
        "query": text("""
            SELECT
                COUNT(DISTINCT product_id) AS total_products
            FROM products;
        """)
    },

    "items_sold": {
        "keywords": ["items", "sold", "total"],
        "query": text("""
            SELECT
                COUNT(*) AS items_sold
            FROM order_items;
        """)
    },

    "average_delivery_days": {
        "keywords": ["average", "delivery", "days"],
        "query": text("""
            SELECT
                AVG(
                    DATEDIFF(
                        order_delivered_customer_date,
                        order_purchase_timestamp
                    )
                ) AS average_delivery_days
            FROM orders
            WHERE order_delivered_customer_date IS NOT NULL;
        """)
    },

    "total_payment_value": {
        "keywords": ["total", "payment"],
        "query": text("""
            SELECT
                SUM(payment_value) AS total_payment_value
            FROM order_payments;
        """)
    },

    "average_payment_value": {
        "keywords": ["average", "payment"],
        "query": text("""
            SELECT
                AVG(payment_value) AS average_payment_value
            FROM order_payments;
        """)
    },

    "average_review_score": {
        "keywords": ["average", "review", "score", "overall"],
        "query": text("""
            SELECT
                AVG(review_score) AS average_review_score
            FROM order_reviews;
        """)
    },

    "review_count": {
        "keywords": ["total", "reviews"],
        "query": text("""
            SELECT
                COUNT(*) AS review_count
            FROM order_reviews;
        """)
    },

    "highest_revenue_state": {
        "keywords": ["highest", "revenue", "state"],
        "query": text("""
            SELECT
                c.customer_state AS state,
                SUM(oi.price) AS revenue
            FROM customers c
            JOIN orders o
                ON c.customer_id = o.customer_id
            JOIN order_items oi
                ON o.order_id = oi.order_id
            GROUP BY c.customer_state
            ORDER BY revenue DESC
            LIMIT 1;
        """)
    },

    "highest_revenue_category": {
        "keywords": ["highest", "revenue", "category"],
        "query": text("""
            SELECT
                COALESCE(
                    t.product_category_name_english,
                    p.product_category_name,
                    'Unknown'
                ) AS category,
                SUM(oi.price) AS revenue
            FROM order_items oi
            JOIN products p
                ON oi.product_id = p.product_id
            LEFT JOIN product_category_name_translation t
                ON p.product_category_name = t.product_category_name
            GROUP BY category
            ORDER BY revenue DESC
            LIMIT 1;
        """)
    },

    "highest_revenue_product": {
        "keywords": ["highest", "revenue", "product"],
        "query": text("""
            SELECT
                oi.product_id,
                SUM(oi.price) AS revenue
            FROM order_items oi
            GROUP BY oi.product_id
            ORDER BY revenue DESC
            LIMIT 1;
        """)
    },

    "most_common_payment_method": {
        "keywords": ["most", "common", "payment", "method"],
        "query": text("""
            SELECT
                payment_type,
                COUNT(*) AS payment_count
            FROM order_payments
            GROUP BY payment_type
            ORDER BY payment_count DESC
            LIMIT 1;
        """)
    },

    "highest_selling_category": {
        "keywords": ["category", "sold", "most"],
        "query": text("""
            SELECT
                p.product_category_name AS category,
                COUNT(*) AS items_sold
            FROM order_items oi
            JOIN products p
                ON oi.product_id = p.product_id
            GROUP BY p.product_category_name
            ORDER BY items_sold DESC
            LIMIT 1;
        """)
    },

    "highest_order_state": {
        "keywords": ["highest", "orders", "state"],
        "query": text("""
            SELECT
                c.customer_state AS state,
                COUNT(DISTINCT o.order_id) AS total_orders
            FROM customers c
            JOIN orders o
                ON c.customer_id = o.customer_id
            GROUP BY c.customer_state
            ORDER BY total_orders DESC
            LIMIT 1;
        """)
    },

    "highest_payment_method": {
        "keywords": ["highest", "payment", "method"],
        "query": text("""
            SELECT
                payment_type,
                SUM(payment_value) AS payment_value
            FROM order_payments
            GROUP BY payment_type
            ORDER BY payment_value DESC
            LIMIT 1;
        """)
    },

    "longest_delivery_state": {
        "keywords": ["longest", "delivery", "state"],
        "query": text("""
            SELECT
                c.customer_state AS state,
                AVG(
                    DATEDIFF(
                        o.order_delivered_customer_date,
                        o.order_purchase_timestamp
                    )
                ) AS average_delivery_days
            FROM customers c
            JOIN orders o
                ON c.customer_id = o.customer_id
            WHERE o.order_delivered_customer_date IS NOT NULL
            GROUP BY c.customer_state
            ORDER BY average_delivery_days DESC
            LIMIT 1;
        """)
    },

    "highest_revenue_month": {
        "keywords": ["highest", "revenue", "month"],
        "query": text("""
            SELECT
                DATE_FORMAT(
                    o.order_purchase_timestamp,
                    '%Y-%m'
                ) AS month,
                SUM(oi.price) AS revenue
            FROM orders o
            JOIN order_items oi
                ON o.order_id = oi.order_id
            GROUP BY month
            ORDER BY revenue DESC
            LIMIT 1;
        """)
    },

    "highest_review_state": {
        "keywords": ["highest", "review", "state"],
        "query": text("""
            SELECT
                c.customer_state AS state,
                AVG(r.review_score) AS average_review_score
            FROM customers c
            JOIN orders o
                ON c.customer_id = o.customer_id
            JOIN order_reviews r
                ON o.order_id = r.order_id
            GROUP BY c.customer_state
            ORDER BY average_review_score DESC
            LIMIT 1;
        """)
    }
}


def identify_question(question):

    question = question.lower()

    for character in "?!.,;:":
        question = question.replace(character, "")

    question_words = set(question.split())

    for question_type, question_data in questions.items():

        keywords = question_data["keywords"]

        if all(
            keyword in question_words
            for keyword in keywords
        ):
            return question_type

    return None


def get_verified_data(question_type):
    """Retrieve the verified metric for a supported question from MySQL."""
    query = questions[question_type]["query"]

    with engine.connect() as connection:
        result = connection.execute(query)
        row = result.fetchone()

    if row is None:
        return None

    result_data = dict(row._mapping)

    for metric, value in result_data.items():
        if value is None:
            return None

    return result_data


def process_question(question):
    """Run the full database-to-Groq workflow.

    Returns: question_type, verified_data, validated_insight, usage_data, error.
    """
    question = question.strip()

    if not question:
        return None, None, None, None, "Please enter a business question."

    question_type = identify_question(question)
    if question_type is None:
        return None, None, None, None, "This question is not currently supported."

    try:
        result_data = get_verified_data(question_type)
    except SQLAlchemyError as error:
        # Do not send a prompt to Groq when verified database retrieval fails.
        print(f"Database error: {error}")
        return None, None, None, None, "Unable to retrieve verified data from the database. Check the database connection."

    if result_data is None:
        return question_type, None, None, None, "No valid data was found for this question."

    result_json = json.dumps(result_data, indent=2, default=str)
    prompt = f"""
User question:
{question}

Verified result retrieved from MySQL:
{result_json}

Task:
Create a concise business insight using only the verified result above.
Return the required JSON fields: summary, key_points, and recommendation.
Do not calculate anything new or add unsupported information.
"""

    try:
        insight, usage_data = ask_llm(prompt)
        return question_type, result_data, insight, usage_data, None
    except RuntimeError as error:
        return question_type, result_data, None, None, str(error)


def main():
    question = input("Ask a business question: ").strip()
    question_type, result_data, insight, usage_data, error = process_question(question)

    if error:
        print(error)
        return

    print("Question Type:", question_type)
    print("Verified Data:")
    print(json.dumps(result_data, indent=2, default=str))
    print("\nAI Insight:")
    print(insight.model_dump_json(indent=2))
    if usage_data:
        print("\nToken and Cost Usage:")
        print(json.dumps(usage_data, indent=2))


if __name__ == "__main__":
    main()
