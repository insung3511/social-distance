from flask import render_template
from flask import Response
from flask import Flask
import cv2

app = Flask(__name__)

cap = cv2.VideoCapture(0)

def generate_frame():
    while True:
        frame = cap.read()
        if not frame:
            break

        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield(b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    retrun render_template('streaming2.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
