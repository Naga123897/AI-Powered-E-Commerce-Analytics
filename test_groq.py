import os # Access environment variables
from dotenv import load_dotenv # Load environment variables from .env file
from openai import OpenAI

# Step 1: Load environment variables from .env file
load_dotenv()

# Step 2: Get the Groq API Key
api_key = os.getenv("GROQ_API_KEY") # os.getenv()- Reads your Groq API Key

if not api_key:
    raise ValueError("GROQ_API_KEY is not found")

# Step 3: Connect to Groq
client = OpenAI(
    api_key = api_key,
    base_url = "https://api.groq.com/openai/v1"
) # OpenAI() Creates the API client And base_url it connects the client to Groq instead of OpenAI

# Step 4: Select the model
MODEL_NAME = "openai/gpt-oss-20b" # Select the Groq Model

# Step 5: Send a test request
response = client.chat.completions.create(
    model = MODEL_NAME,
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain e-commerce analytics in simple English in two sentences."}
    ]
) # Messages - Contains system and user prompts
# Create() - Sends the request to the Groq API and returns the response


# Step 6: Display the response
print("\nGroq API Connection Successful!")
print("\nModel Response:")
print(response.choices[0].message.content) # Gets the first generated response
