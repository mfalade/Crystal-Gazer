import json
import csv
from flask import (Flask, redirect, render_template, request, url_for)

from .gazer import Gazer

app = Flask(__name__)

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
    verdict, csv_data = crystal_gazer.get_prediction_for_data(csv_file.stream)
    results = verdict.values.tolist()
    correct = 0
    for x in range(0, len(results)):
        if csv_data["Bootcamp"][x] == int(round(results[x][3])):
            correct = correct + 1

    accuracy = (float(correct) / float(len(results))) * 100
    return render_template(
        "result.html",
        file_name=file_name,
        results=results,
        accuracy=round(accuracy, 2)
    )
