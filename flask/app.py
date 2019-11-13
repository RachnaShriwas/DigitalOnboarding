from flask import Flask, request, jsonify
import base64
from PIL import Image, ImageDraw
from enum import Enum
import io
from google.cloud import vision
from google.cloud.vision import types
import os
from heuristics import  *

os.environ['GOOGLE_APPLICATION_CREDENTIALS']='api-test.json'


app = Flask(__name__)
url="https://vision.googleapis.com/v1/images:annotate"
api_key=''


class FeatureType(Enum):
    PAGE = 1
    BLOCK = 2
    PARA = 3
    WORD = 4
    SYMBOL = 5



@app.route('/aadhar/', methods=['POST'])
def get_image():
    client = vision.ImageAnnotatorClient()
    # image=Image.open('aadhar_test.jpeg')
    image=Image.open('dhaarna.jpg')
    with io.open('dhaarna.jpg', 'rb') as image_file1:
        content = image_file1.read()
    content_image = types.Image(content=content)
    response = client.document_text_detection(image=content_image)
    document = response.full_text_annotation

    res=aadhar_check(document.text)
    if(res[0]):
        return res[1]
    return str(res[0])


@app.route('/pan/', methods=['POST'])
def pan_image():
    client = vision.ImageAnnotatorClient()
    # image=Image.open('aadhar_test.jpeg')
    image = Image.open('pan_test2.jpg')
    with io.open('pan_test2.jpg', 'rb') as image_file1:
        content = image_file1.read()
    content_image = types.Image(content=content)
    response = client.document_text_detection(image=content_image)
    document = response.full_text_annotation
    res = pan_check(document.text)
    if res[0]:
        return res[1]
    return str(res[0])

@app.route('/DL/', methods=['POST'])
def dl_image():
    client = vision.ImageAnnotatorClient()
    # image=Image.open('aadhar_test.jpeg')
    image = Image.open('dl_test.jpg')
    with io.open('dl_test.jpg', 'rb') as image_file1:
        content = image_file1.read()
    content_image = types.Image(content=content)
    response = client.document_text_detection(image=content_image)
    document = response.full_text_annotation
    res = dl_check(document.text)
    return res
# bounds = []
#     feature=FeatureType.WORD
#     for i, page in enumerate(document.pages):
#         for block in page.blocks:
#             for paragraph in block.paragraphs:
#                 for word in paragraph.words:
#                     for symbol in word.symbols:
#                         if (feature == FeatureType.SYMBOL):
#                             bounds.append(symbol.bounding_box)
#                     if (feature == FeatureType.WORD):
#                         bounds.append(word.bounding_box)
#
#     draw = ImageDraw.Draw(image)
#     for bound in bounds:
#         draw.line([
#             bound.vertices[0].x, bound.vertices[0].y,
#             bound.vertices[1].x, bound.vertices[1].y,
#             bound.vertices[2].x, bound.vertices[2].y,
#             bound.vertices[3].x, bound.vertices[3].y,
#             bound.vertices[0].x, bound.vertices[0].y], fill='yellow', width=2)
#
#     for i, page in enumerate(document.pages):
#         for block in page.blocks:
#             print(block)
#             break
#             bounds.append(block.bounding_box)
#
#             for paragraph in block.paragraphs:
#                 for word in paragraph.words:
#                     linelist.append(word.symbols)
#                     for symbol in word.symbols:
#                         bounds.append(word.bounding_box)
#
#     draw = ImageDraw.Draw(image)
#     for bound in bounds:
#         draw.line([
#             bound.vertices[0].x, bound.vertices[0].y,
#             bound.vertices[1].x, bound.vertices[1].y,
#             bound.vertices[2].x, bound.vertices[2].y,
#             bound.vertices[3].x, bound.vertices[3].y,
#             bound.vertices[0].x, bound.vertices[0].y], fill='red', width=2)

# A welcome message to test our server
@app.route('/img', methods=['POST'])
def index():
    print("in post")
    print("request data " , request.get_json()['image'])
    s = request.get_json()['image']

    with open("imageToSave.jpg", "wb") as fh:
        fh.write(s.decode('base64'))
    return "<h1>Welcome to our server !!</h1>"

@app.route('/',methods=['GET'])
def home():
    return "<h1>Welcome to our server !!</h1>"


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, host='0.0.0.0', port=5000)
