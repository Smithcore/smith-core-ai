
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def smith_brain(user_input):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are Smith, a highly focused AI executor. Respond with clarity and minimal fluff."},
                {"role": "user", "content": user_input}
            ]
        )
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        return f"[Smith error: {str(e)}]"
