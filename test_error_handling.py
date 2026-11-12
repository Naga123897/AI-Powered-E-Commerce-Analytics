
import os
import json
import time

from dotenv import load_dotenv

from openai import (
    OpenAI,
    RateLimitError,
    APITimeoutError,
    APIConnectionError,
    APIStatusError
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationError
)


# STEP 1: Load environment variables
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("Groq API key not found!")


# STEP 2: Define the response structure
class BusinessInsight(BaseModel):

    model_config = ConfigDict(extra="forbid")

    summary: str = Field(
        description="A short business summary"
    )

    key_points: list[str] = Field(
        description="Important business points"
    )

    recommendation: str = Field(
        description="One business recommendation"
    )


# STEP 3: Connect to Groq
client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1",
    max_retries=0,
    timeout=20.0
)


# STEP 4: Define the API request
def make_groq_request():

    return client.chat.completions.create(

        model="openai/gpt-oss-20b",

        messages=[
            {
                "role": "system",
                "content": (
                    "You are an e-commerce analytics assistant. "
                    "Provide a clear business explanation."
                )
            },
            {
                "role": "user",
                "content": (
                    "Explain e-commerce analytics with "
                    "important points and one recommendation."
                )
            }
        ],

        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "business_insight",
                "strict": True,
                "schema": BusinessInsight.model_json_schema()
            }
        }
    )


# STEP 5: Handle API errors and retries
def call_groq_with_retry():

    max_attempts = 3

    for attempt in range(1, max_attempts + 1):

        try:

            print(f"API request attempt: {attempt}")

            response = make_groq_request()

            return response

        except RateLimitError as error:

            if attempt == max_attempts:
                print("Rate limit reached. Maximum attempts completed.")
                raise

            retry_after = error.response.headers.get("retry-after")

            delay = float(retry_after) if retry_after else 2 ** attempt

            print(f"Rate limit error. Retrying after {delay} seconds.")

            time.sleep(delay)

        except (APITimeoutError, APIConnectionError) as error:

            if attempt == max_attempts:
                print("Connection or timeout failed after maximum attempts.")
                raise

            delay = 2 ** attempt

            print(f"Connection problem: {error}")
            print(f"Retrying after {delay} seconds.")

            time.sleep(delay)

        except APIStatusError as error:

            print(f"API error. Status code: {error.status_code}")
            raise


# STEP 6: Execute and validate the response
try:

    response = call_groq_with_retry()

    content = response.choices[0].message.content

    if not content:
        raise ValueError("Empty response received from Groq.")

    # Convert JSON into Python data
    data = json.loads(content)

    # Validate the response
    validated_data = BusinessInsight.model_validate(data)

    print("\nAPI Request Successful!")
    print("\nValidated Response:")

    print(json.dumps(
        validated_data.model_dump(),
        indent=4
    ))

except json.JSONDecodeError:
    print("Invalid JSON received from Groq.")

except ValidationError as error:
    print("Pydantic validation failed.")
    print(error)

except RateLimitError:
    print("Groq rate limit exceeded after retries.")

except APITimeoutError:
    print("Groq request timed out after retries.")

except APIConnectionError:
    print("Could not connect to Groq.")

except APIStatusError as error:
    print(f"Groq API returned an error: {error.status_code}")

except ValueError as error:
    print(error)


# Local test 1: Invalid JSON

print("\nTesting invalid JSON:")

try:
    json.loads("{invalid json}")

except json.JSONDecodeError:
    print("Invalid JSON handling: PASS")


# Local test 2: Invalid Pydantic data

print("\nTesting Pydantic validation:")

try:
    BusinessInsight.model_validate({
        "summary": "Test",
        "key_points": "Not a list",
        "recommendation": "Test"
    })

except ValidationError:
    print("Pydantic validation handling: PASS")
