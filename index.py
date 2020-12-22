from flask import Flask, render_template
import main

app = Flask(__name__)

@app.route('/')
def Defaultindex():
    return render_template('index.html')

@app.route('/front/status.html')
def Statusindex():
    return render_template('front/status.html', peopleCount_PythonWebpage=main.warnPeople, allpeople_Count=main.wholePeople, result=main.noneCompliance)

@app.route('/front/streaming.html')
def Streamingindex():
    return render_template('front/streaming.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=4343, debug=True)