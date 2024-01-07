from flask import Flask, request, jsonify
import openai

openai.api_key = "" # replace with your key

app = Flask(__name__)

@app.route('/generate_values')
def generate_values():
    message = request.args.get("message")
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "The following is a conversation with an business man. You are a computer that correlates ideas to how it affects certain environmental resources. Return the resources that are affected by the idea. Try to think of more than 4 resources, ideally 16. Negative numbers mean that it would negatively affect the resource, and positive numbers mean that it would positively affect the resource. 0 means that it would not majorly affect the resource."
            },
            {
                "role": "assistant",
                "content": "metal: -1, reusability: 1, sustainability: 1, wood: 0"
            },
            {
                "role": "user",
                "content": message
            },
        ],
        temperature=0.7,
        max_tokens=64
    )

    return str(response.choices[0].message.content)

