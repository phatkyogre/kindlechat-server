A tiny, lightweight texting system designed specifically so two Kindles can message each other, using a super-simple Flask backend and a Kindle client script.

📌 Overview

KindleChat is a minimal messaging system made for e-ink devices like the Kindle (using KOReader or Python hacks). It has:

A simple Python/Flask server to store & forward messages

A client script that your Kindle can run to send/receive messages

Optional: host the server online (Railway/Vercel/Render) so you and your friend can text anywhere

📁 Project Structure
kindletext/
│
├── server/
│   ├── app.py            # Flask API
│   ├── requirements.txt
│   └── messages.json     # stored messages
│
└── client/
    └── client.py         # Kindle client that sends/receives messages

🖥️ Server Setup (Flask)

server/app.py

from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

MESSAGES = []

@app.route("/send", method=["POST"])
def send():
    data = request.json
    msg = {
        "sender": data.get("sender"),
        "text": data.get("text"),
        "ts": datetime.utcnow().isoformat()
    }
    MESSAGES.append(msg)
    return jsonify({"status": "ok"}), 200

@app.route("/messages", methods=["GET"])
def messages():
    return jsonify(MESSAGES), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

requirements.txt
flask

📱 Kindle Client Setup

This is a lightweight script your Kindle runs using KOReader's terminal or Python environment.

client/client.py

import requests
import time

SERVER = "https://yourserverurl.com"

NAME = input("Your name: ")

def send_msg():
    text = input("Message: ")
    requests.post(SERVER + "/send", json={
        "sender": NAME,
        "text": text
    })

def show_msgs():
    msgs = requests.get(SERVER + "/messages").json()
    print("\n--- Messages ---")
    for m in msgs:
        print(f"[{m['sender']}] {m['text']}")

while True:
    print("\n1 = Send   2 = Refresh")
    choice = input("> ")

    if choice == "1":
        send_msg()
    if choice == "2":
        show_msgs()

    time.sleep(0.5)

🚀 How to Deploy Online (Free)
Railway (recommended and easy)

Create a Railway account

Click New Project → Deploy from Repo

Select your KindleChat folder

Set the server to run:

python server/app.py


Railway gives you a free HTTPS URL

Put that URL into SERVER = "" in the Kindle client script

📡 How Texting Works

Your Kindle sends a POST to /send

Server stores the message

The other Kindle refreshes /messages to read it

Works with two people, no database required, no images, no typing indicators — super clean and simple

📝 Notes

Texts persist until you reboot the server

You can add user filtering later if you want private inboxes


yes i had chatgpt make this readme
KOReader can run Python scripts just fine

Works on Kindle Basic, Paperwhite, Oasis, etc.
