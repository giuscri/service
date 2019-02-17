from flask import Flask, jsonify, request
from google.cloud import vision
from os import environ
import json, re
from datetime import datetime

def text_detection(blob):
    client = vision.ImageAnnotatorClient()
    image = vision.types.Image(content=blob)
    return client.text_detection(image=image)

def parse_detected_front_text(detected_front_text):
    municipality_match = re.search(r"MUNICIPALITY\n([A-Z]+)", detected_front_text)
    if municipality_match:
        municipality = municipality_match.group(1)
    else:
        municipality = None

    name_match = re.search(r"SURNAME\n([A-Z]+)\n(?:NOME/NAME\n)?([A-Z]+)", detected_front_text)
    if name_match:
        last_name, first_name = name_match.group(1, 2)
    else:
        last_name, first_name = None, None

    birth_match = re.search(r"OF BIRTH\n([A-Z]+ \([A-Z]{2,4}\)) (\d\d\.\d\d\.\d\d\d\d)", detected_front_text)
    if birth_match:
        place_of_birth, date_of_birth = birth_match.group(1, 2)
        try:
            date_of_birth = datetime.strptime(date_of_birth, "%d.%m.%Y").date().isoformat()
        except ValueError:
            pass
    else:
        place_of_birth, date_of_birth = None, None

    sex_match = re.search(r"SEX\n([A-Z])\n(?:STATURA)", detected_front_text) 
    if sex_match:
        sex = sex_match.group(1)
    else:
        sex = None

    height_match = re.search(r"HEIGHT\n([0-9]{3})", detected_front_text)
    if height_match:
        height = height_match.group(1)
    else:
        height = None

    nationality_match = re.search(r"NATIONALITY\n([A-Z]+)", detected_front_text)
    if nationality_match:
        nationality = nationality_match.group(1)
    else:
        nationality = None

    expiration_date_match = re.search(r"EXPIRY\n(\d\d\.\d\d\.\d\d\d\d)", detected_front_text)
    if expiration_date_match:
        expiration_date = expiration_date_match.group(1)
        try:
            expiration_date = datetime.strptime(expiration_date, "%d.%m.%Y").date().isoformat()
        except ValueError:
            pass
    else:
        expiration_date = None

    issue_date_match = re.search(r"ISSUING\n(\d\d\.\d\d\.\d\d\d\d)", detected_front_text)
    if issue_date_match:
        issue_date = issue_date_match.group(1)
        try:
            issue_date = datetime.strptime(issue_date, "%d.%m.%Y").date().isoformat()
        except ValueError:
            pass
    else:
        issue_date = None

    return {
        "municipality": municipality,
        "last_name": last_name,
        "first_name": first_name,
        "place_of_birth": place_of_birth,
        "date_of_birth": date_of_birth,
        "sex": sex,
        "height": height,
        "nationality": nationality,
        "expiration_date": expiration_date,
        "issue_date": issue_date,
    }

app = Flask(__name__)

@app.route("/")
def root():
    return jsonify({
        "commands": [
            {
                "help": "POST front of card as the blob to extract text",
                "methods": ["POST"],
                "endpoint": "/front"
            }
        ]
    })

@app.route("/front", methods=["POST"])
def post_front():
    content = request.data
    vision_api_response = text_detection(content)
    detected_front_text = vision_api_response.full_text_annotation.text
    parsed_detected_front_text = parse_detected_front_text(detected_front_text)
    return jsonify(parsed_detected_front_text)

if __name__ == "__main__":
    app.run()