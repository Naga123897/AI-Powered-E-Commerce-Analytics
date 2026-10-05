import os
import ollama
import json
from sqlalchemy import text
from src.database import engine

ollama_client = ollama.Client(
    host=os.getenv("OLLAMA_HOST", "http://localhost:11434")
)


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
"""


def ask_llm(prompt):
    response = ollama_client.chat(
        model="qwen3:1.7b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]


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

    question = question.strip()

    if not question:
        return None, None, "Please enter a business question."

    question_type = identify_question(question)

    if question_type is None:
        return None, None, "This question is not currently supported."

    result_data = get_verified_data(question_type)

    if result_data is None:
        return None, None, "No valid data was found for this question."

    result_json = json.dumps(
        result_data,
        indent=2,
        default=str
    )

    prompt = f"""
{BASE_PROMPT}

User question:
{question}

Verified result from MySQL:
{result_json}

Task:
Answer the user's question using only the verified result above.

Additional rules:
- Do not calculate anything new.
- Do not create ratios or percentages.
- Do not add information that is not in the result.
- Keep the answer short and clear.
"""

    answer = ask_llm(prompt)

    return question_type, result_data, answer


def main():

    question = input("Ask a business question: ").strip()

    if not question:
        print("Please enter a business question.")
        return

    question_type, result_data, answer = process_question(question)

    if question_type is None:
        print(answer)
        return

    print("Question Type:", question_type)

    print("Verified Data:")

    print(
        json.dumps(
            result_data,
            indent=2,
            default=str
        )
    )

    print()
    print("AI Answer:")
    print(answer)


if __name__ == "__main__":
    main()