import os

import openai
import json
import logging
from logging import FileHandler
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        question = request.form["question"]
        result = ''
        app.logger.info("question: %s" % question)
        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                # model="text-curie-001",
                # model="text-babbage-001",
                # model="text-ada-001",
                prompt=generate_prompt(question),
                temperature=0.6,
                max_tokens=512,
            )
            app.logger.info("response: %s" % response)
            result = response.choices[0].text
            app.logger.info("result: %s" % result)
        except openai.error.APIError as e:
            result = f"OpenAI API returned an API Error: {e}" 
            app.logger.error(result)
        except openai.error.APIConnectionError as e:
            result = f"Failed to connect to OpenAI API: {e}"
            app.logger.error(result)
        except openai.error.RateLimitError as e:
            result = f"OpenAI API request exceeded rate limit: {e}"
            app.logger.error(result)
        return redirect(url_for("index", question=question, result=result))

    result = request.args.get("result")
    question = request.args.get("question")
    return render_template("index.html", question=question, result=result)


def generate_prompt(question):
    return question

if __name__ == '__main__':
    logHandler = logging.FileHandler('flask.log')
    app.logger.addHandler(logHandler)
    app.run(host='0.0.0.0', port=8081, debug=True)
