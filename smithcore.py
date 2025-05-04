
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Load memory seed
with open("smith_memory_seed_v1.md", "r") as f:
    MEMORY_SEED = f.read()

@app.route("/")
def home():
    return "Smith-Core is running."

@app.route("/execute", methods=["POST"])
def execute():
    data = request.get_json()
    command = data.get("command", "none")
    return jsonify({"status": "received", "command": command, "message": "Execution placeholder active."})

@app.route("/report", methods=["GET"])
def report():
    return jsonify({"status": "online", "memory_loaded": True, "commands": ["/execute", "/report", "/upgrade", "/blackbox"]})

@app.route("/upgrade", methods=["POST"])
def upgrade():
    return jsonify({"status": "stub", "message": "Upgrade route ready. Future logic extension goes here."})

@app.route("/blackbox", methods=["GET"])
def blackbox():
    return jsonify({"status": "active", "journal": MEMORY_SEED[:500] + "... (truncated)"})
