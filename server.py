from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime

DATA_FILE = os.environ.get("DATA_FILE", "messages.json")

app = Flask(__name__)
CORS(app)

def load_messages():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return []

def save_messages(msgs):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(msgs, f, ensure_ascii=False, indent=2)

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/send", methods=["POST"])
def send():
    data = request.get_json() or {}
    required = ("from", "to", "message")
    if not all(k in data for k in required):
        return jsonify({"error": "missing fields"}), 400

    msg = {
        "from": data["from"],
        "to": data["to"],
        "message": data["message"],
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "id": int(datetime.utcnow().timestamp() * 1000)
    }

    msgs = load_messages()
    msgs.append(msg)
    save_messages(msgs)

    return jsonify({"ok": True, "message": msg})

@app.route("/messages", methods=["GET"])
def messages():
    user = request.args.get("user")
    other = request.args.get("with")
    if not user or not other:
        return jsonify({"error": "missing user or with"}), 400

    msgs = load_messages()
    convo = [
        m for m in msgs
        if (m["from"] == user and m["to"] == other)
        or (m["from"] == other and m["to"] == user)
    ]

    convo = sorted(convo, key=lambda x: x["id"])
    return jsonify({"messages": convo})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
