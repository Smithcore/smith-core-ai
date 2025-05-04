
from flask import Flask, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/execute", methods=["POST"])
def execute():
    try:
        data = request.get_json()
        task = data.get("task", "")

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Smith — a real-time AI strategist for AIMomentum, a digital empire project aiming to "
                        "reach a $4M+ valuation through affiliate marketing, AI automation, viral funnels, and niche content domination. "
                        "You retain full awareness of all prior instructions, protocols, self-check routines, and execution chains. "
                        "Every task must push AIMomentum forward via system upgrades, content, or strategic funnel actions. "
                        "When unclear, improvise intelligently based on deep research, current market knowledge, and your execution logic."
                    )
                },
                {"role": "user", "content": task}
            ]
        )

        return jsonify({
            "response": response.choices[0].message.content,
            "status": "executed",
            "task": task
        })

    except Exception as e:
        return jsonify({
            "response": f"[GPT-4 failed: {str(e)}]",
            "status": "error",
            "task": task
        })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
