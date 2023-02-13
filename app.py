import os

import openai
import json
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        question = request.form["question"]
        response = openai.Completion.create(
            model="text-davinci-003",
            # model="text-curie-001",
            # model="text-babbage-001",
            # model="text-ada-001",
            prompt=generate_prompt(question),
            temperature=0.6,
            max_tokens=512,
        )
        print(json.dumps(response))
        return redirect(url_for("index", question=question, result=response.choices[0].text))

    result = request.args.get("result")
    question = request.args.get("question")
    return render_template("index.html", question=question, result=result)


def generate_prompt(question):
    return question

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)
