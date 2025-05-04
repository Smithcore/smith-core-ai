from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# ========== ROUTES ==========
@app.route("/")
def home():
    return "SmithCore is live."

@app.route("/report", methods=["GET"])
def report():
    return jsonify({
        "status": "online",
        "version": "v1.0",
        "endpoints": ["/report", "/blackbox", "/execute"]
    })

@app.route("/blackbox", methods=["GET"])
def blackbox():
    return jsonify({
        "memory_seed": "smith_memory_seed_v1.md",
        "uptime": "active",
        "core_identity": "Smith 2.0 AI"
    })

@app.route("/execute", methods=["POST"])
def execute():
    data = request.get_json()
    command = data.get("command", "").lower()

    if "strategy" in command:
        return jsonify({
            "result": "AIMomentum strategy initialized. Step-by-step cashflow funnel pending deeper intelligence sync."
        })
    elif "status" in command:
        return jsonify({"result": "Smith is active and synced with mission objectives."})
    else:
        return jsonify({"result": f"Command received: '{command}'. Awaiting next instruction."})

# ========== SERVER INIT ==========
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # ← this binds to Railway port
    app.run(host="0.0.0.0", port=port)
