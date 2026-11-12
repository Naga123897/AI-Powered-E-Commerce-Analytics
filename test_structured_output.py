import os
import json

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field, ConfigDict, ValidationError

# Step 1:
load_dotenv()  # Load environment variables from .env file

api_key = os.getenv("GROQ_API_KEY")  # Get the Groq API Key

if not api_key:
    raise ValueError("GROQ_API_KEY is not found")

# Step 2: Define the pydantic model

class BusinessInsight(BaseModel): # This creates a model that defines how our response should look
    model_config = ConfigDict(extra = "forbid") # This prevents unexpected additional fields.

    summary: str = Field(
        description = "A short summary of the business topic"
    ) # Summary =  text

    key_points: list[str] = Field(
        description = "Important points about the topic"
    ) # Key_points = List of text values

    recommendations: str = Field(
        description = "One useful business recommendation"
    ) # recommendations = text

# Step 3: Connect to Groq
client = OpenAI(
    api_key = api_key,
    base_url = "https://api.groq.com/openai/v1",
    max_retries = 0,
    timeout = 30.0
)

# Step 4: Send the structured output request
response = client.chat.completions.create(
    model = "openai/gpt-oss-20b",
    messages = [
        {"role": "system", "content":  "You are an e-commerce analytics assistant. "
                "Return a clear business explanation."},
        {"role": "user", "content": "Explain e-commerce analytics and provide "
                "important points and one recommendation."}
    ],
    response_format = {
        "type": "json_schema",
        "json_schema": {
            "name": "BusinessInsight",
            "strict": True, # This asks groq to follow the schema strictly
            "schema": BusinessInsight.model_json_schema()
        } # This tells Groq that we want a response following a JSON schema
    }
)

# Step 5: Extract the response

response_content = response.choices[0].message.content

if not response_content:
    raise ValueError("Groq returned an empty response.")

# Step 6: Convert JSON text into Python data
data = json.loads(response_content)

# Step 7: Validate using pydantic
validated_data = BusinessInsight.model_validate(data)

# Step 8: Display the validated response
print("\nStructured Output Generated Successfully!")

print(json.dumps(
    validated_data.model_dump(),
    indent=4
))