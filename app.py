from flask import Flask, render_template, request, jsonify
import time
from openai import OpenAI

app = Flask(__name__)

# Enter your Assistant ID here.
ASSISTANT_ID = "asst_DNTuOIVN1F38xhx47zlpICtu"

# Make sure your API key is set as an environment variable.
client = OpenAI(api_key="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")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json["message"]

    thread = client.beta.threads.create(messages=[{"role": "user", "content": user_input}])
    run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=ASSISTANT_ID)

    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        time.sleep(1)

    message_response = client.beta.threads.messages.list(thread_id=thread.id)
    messages = message_response.data
    latest_message = messages[0]

    return jsonify({"message": latest_message.content[0].text.value})

if __name__ == "__main__":
    app.run(debug=True)
