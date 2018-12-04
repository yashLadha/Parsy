import os
import requests
from dotenv import load_dotenv
from flask import Flask, request

load_dotenv()

app = Flask(__name__)

PAGE_ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
FB_API_URL = os.getenv('FB_API_URL')


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/webhook', methods=['GET'])
def verify_webhook():
    if request.args.get('hub.verify_token') == os.getenv('VERIFY_TOKEN'):
        return request.args.get('hub.challenge')
    return "Invalid token"


def detect_text(uri):
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()
    response = requests.get(uri)
    image = vision.types.Image(content=response.content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    string = texts[0].description
    return string


def send_message(psid, ocr_message):
    payload = {
        'message': {
            'text': ocr_message
        },
        'recipient': {
            'id': psid
        },
        'notification_type': 'REGULAR'
    }
    auth = {
        'access_token': PAGE_ACCESS_TOKEN
    }
    response = requests.post(FB_API_URL, params=auth, json=payload)
    return response.json()


@app.route('/webhook', methods=['POST'])
def listen():
    json_res = request.json
    payload = json_res['entry']
    for entries in payload:
        # Checks for the text message event
        if 'message' in entries:
            psid = entries['sender']['id']
            text_message = entries['message']['text']
            response = send_message(psid, "Please upload an image")
            print('Response ', response)

        # Checks for the attachment message event
        if 'messaging' in entries:
            for attach in entries['messaging']:
                psid = attach['sender']['id']
                if 'message' in attach:
                    if 'attachments' in attach['message']:
                        for resource in attach['message']['attachments']:
                            # Image attachment for scrapping
                            if resource['type'] == 'image':
                                # Fetch the payload url
                                if 'payload' in resource:
                                    image_url = resource['payload']['url']
                                    ocr_message = detect_text(image_url)
                                    response = send_message(psid, ocr_message)
                                    print('Response ', response)
    return 'Processed Response'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000')
