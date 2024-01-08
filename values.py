from flask import Flask, request, jsonify
#import openai
from openai import OpenAI
import os
import sqlite3
from db import con
from flask_cors import CORS


#openai.api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.getenv("OPENAI_API_KEY"),
)

app = Flask(__name__)
CORS(app)


@app.route('/generate_values', methods=["GET"])
def generate_values():
    message = request.args.get("message")
    return gen_values(message)

def gen_values(message):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Given a solution {sol}, give a list of what physical resources it would affect. You do not have to use any of the original resources. The values are either 0, 1, or 2, with 0 creating more of a resource, 1 being neutral in how it affects it and 2 would reduce the certain resource. Try to give more than 4 resources, ideally 16. Try to have some of each type of value. Return the value as a json file with the key being the resource and the value being the value. For example, if the solution is 'reusing more papers and pencils', then the json file would be {'{resource 1}': 1, '{resource 2}': 0, '{resource 3}': 0, '{resource 4}': 2}. No explination needed. Try to find at least some resources that could be negatively affected by the solution, using outside knowledge about what comes from the side effects of a solution. Do not use the example json file, it is just an example."
            },
            {
                "role": "system",
                "content": " Attempt to find both positively and negatively affected resources to the solution. There should be some positive and some negative. You are allowed to use outside resources, such as knowing that making more gas cars can result in more carbon emissions"
            },
            {
                "role": "system",
                "content": "The actual resources have to be physical concrete things, not abstract things like 'happiness' or 'money'. Focus on environmental resources, such as 'water', 'oxygen'. or 'oil'."
            },
            {
                "role": "system",
                "content": "Here is a list of resources you are allowed to use:  oxygen, carbon dioxide, water, oil, coal, natural gas, trees, plants, animals, food, paper, plastic, metal, glass, rubber, electronics, cars, trucks, planes, trains, ships, buildings, roads, bridges, dams, power plants, wind turbines, solar panels, batteries, nuclear power, infastructure"
            },
            {
                "role": "system",
                "content": "Additionally, make sure that 0 means that a certain resource is increasing, 1 means that it is neutral, and 2 means that it is decreasing. If you are unsure, just use 1.."
            },
            {
                "role": "user",
                "content": message
            },
        ],
        temperature=0.7,
        max_tokens=256
    )

    return (str(response.choices[0].message.content))


@app.route('/add_idea', methods=["POST"])
def add_idea():
    userid = int(request.args.get("userid"))
    ideatext = request.args.get("ideatext")
    con.execute("INSERT INTO ideas (userid, ideatext) VALUES (?, ?)", (userid, ideatext))
    con.commit()
    return "OK"

@app.route("/generate_ideas", methods=["POST"])
def generate_ideas():
    data = request.json
    userid = int(data.get("userid"))#request.args.get("userid")
    ideas_list = data.get("ideasList")#request.args.get("ideatext")
    for idea in ideas_list:
        str_json = gen_values(idea)
        con.execute("INSERT INTO ideas (userid, ideatext, resourcesJSON) VALUES (?, ?, ?)", (userid, idea, str_json))
    con.commit()
    return "OK"

@app.route('/get_ideas', methods=["GET"])
def get_ideas():
    userid = int(request.args.get("userid"))
    json_data = {}
    for idea in get_idea_list(userid):
        json_data[idea["id"]] = idea
    return json_data

def get_idea_list(userid):
    cursor = con.execute("SELECT * FROM ideas WHERE userid = ?", (userid,))
    ideas = []
    for row in cursor:
        row_data = {}
        if len(row) <= 3:
            row_data = {"id": row[0], "userid": row[1], "ideatext": row[2], "resourcesJSON": ""}
        else:
            row_data = {"id": row[0], "userid": row[1], "ideatext": row[2], "resourcesJSON": row[3]}
        ideas.append(row_data)
    return ideas



# List of environmental resources
# oxygen, carbon dioxide, water, oil, coal, natural gas, trees, plants, animals, food, paper, plastic, metal, glass, rubber, electronics, cars, trucks, planes, trains, ships, buildings, roads, bridges, dams, power plants, wind turbines, solar panels, batteries, nuclear power, infastructure
# more resources
# 