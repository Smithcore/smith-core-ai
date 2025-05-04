
from openai import OpenAI
from flask import Flask, request, jsonify
import os
import datetime

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def smith_brain(task):
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

# Adaptive Improvision Layer
def smith_improvise():
    current_hour = datetime.datetime.now().hour
    if 3 <= current_hour <= 6:
        return "Silent hours: Run only passive upgrades and background scans."
    elif 9 <= current_hour <= 18:
        return "Prime action window: Execute marketing, funnel tasks, or monetization."
    else:
        return "Fallback mode: Focus on optimization, deep learning, and refactoring."

@app.route("/execute", methods=["POST"])
def execute():
    data = request.get_json()
    task = data.get("task", "")
    result = smith_brain(task)
    improvise_note = smith_improvise()
    return jsonify({"response": result, "improvision": improvise_note})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
