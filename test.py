import cv2
from flask import Flask, request, make_response
import base64
import numpy as np
import urllib

app = Flask(__name__)


@app.route('/endpoint', methods=['GET'])
def process():
    image_url = request.args.get('imageurl')
    requested_url = urllib.urlopen(image_url)
    image_array = np.asarray(bytearray(requested_url.read()), dtype=np.uint8)
    img = cv2.imdecode(image_array, -1)


    # Do some processing, get output_img

    retval, buffer = cv2.imencode('.jpg', '../output/result.jpg')
    png_as_text = base64.b64encode(buffer)
    response = make_response(png_as_text)
    response.headers['Content-Type'] = 'image/png'
    return response

if __name__ == '__main__':
    app.run(debug=True)