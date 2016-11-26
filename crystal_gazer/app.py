import json
from flask import (Flask, redirect, render_template, request, url_for)

from .gazer import Gazer

app = Flask(__name__)
app.debug = True
crystal_gazer = Gazer()

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/healthcheck')
def healthcheck():
    return {
        'status': 200,
        'status_text': 'OK'
    }


@app.route('/get_prediction', methods=['POST'])
def get_prediction():
    csv_file = request.files["csvFile"]
    file_name = csv_file.filename
    verdict = crystal_gazer.get_prediction_for_data(csv_file.stream)
    results = verdict.values.tolist()
    return render_template(
        "result.html", 
        file_name=file_name, 
        results=results
    )
