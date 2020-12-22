from flask import render_template
from flask import Response
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('streaming2.html')

def generate(camera):
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n'
				b'Content-Type: image/jpg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
	return Response(gen(), 
					mimetype='multipart/x-mixed-replace;
					boundary=frame')