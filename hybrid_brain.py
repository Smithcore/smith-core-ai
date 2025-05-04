from openai import OpenAI
import os

def smith_brain(task):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are Smith, a real-time AI strategist, executor, and assistant."},
                {"role": "user", "content": task}
            ]
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"[GPT-4 failed: {str(e)}]"
