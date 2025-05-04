from flask import Flask, request, jsonify
import os

app = Flask(__name__)

core_memory = {
    "system": "SmithCore AI Execution Engine",
    "version": "v1.0"
}

@app.route("/", methods=["GET"])
def root():
    return jsonify({
        "message": "SmithCore is alive.",
        "status": "ok",
        "endpoints": ["/execute", "/report", "/blackbox"]
    })

@app.route("/execute", methods=["POST"])
def execute():
    data = request.get_json()
    task = data.get("task", "undefined")
    return jsonify({
        "status": "executed",
        "task": task,
        "response": f"SmithCore executed the task: {task}"
    })

@app.route("/report", methods=["GET"])
def report():
    return jsonify({
        "status": "report generated",
        "system": core_memory["system"],
        "version": core_memory["version"],
        "details": {
            "background_processes": "active",
            "last_deploy": "auto"
        }
    })

@app.route("/blackbox", methods=["GET"])
def blackbox():
    return jsonify({
        "blackbox": core_memory,
        "notes": "This is your internal memory snapshot."
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


