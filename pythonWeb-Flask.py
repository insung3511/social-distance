from flask import render_template
from flask import Blueprint
from flask import Response
from flask import url_for
from flask import request
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('statusFlask.html')

@app.route('/peopleCount_PythonWebpage')
def text_feed():
    webprint = webpageSender()
    return Response(webprint.printRisk(),
                mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port='8080', debug=True)