from openai import OpenAI
import os

def smith_brain(task):
    try:
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are SmithCore, an execution AI assistant. Respond with clarity and precision."},
                {"role": "user", "content": task}
            ]
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"[GPT fallback failed: {e}]"
