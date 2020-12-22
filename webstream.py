from flask import render_template
from flask import Response
from flask import Flask
import cv2

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('streaming.html')

def gen(cam):
    while True:
        img = cv2.imread('./output/result.jpg')
        _, img_encoded = cv2.imencode('.jpg', img)
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response("./output/result.jpg",
            mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port='8080', debug=True)
