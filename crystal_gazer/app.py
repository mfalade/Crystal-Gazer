import json
import csv
import datetime
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
    start = datetime.datetime.now()
    verdict, csv_data = crystal_gazer.get_prediction_for_data(csv_file.stream)
    end = datetime.datetime.now()
    results = verdict.values.tolist()
    correct = 0
    positives = 0
    negatives = 0
    false_negatives = 0
    false_positives = 0

    for x in range(0, len(results)):
        if csv_data["Bootcamp"][x] == 1:
            positives += 1
        else:
            negatives += 1

        result = int(round(results[x][3]))
        if csv_data["Bootcamp"][x] == result:
            correct += 1
        else:
            if result == 1:
                false_positives += 1
            else:
                false_negatives += 1

    accuracy = (float(correct) / float(len(results))) * 100
    false_negatives = (float(false_negatives) / float(negatives)) * 100
    false_positives = (float(false_positives) / float(positives)) * 100
    return render_template(
        "result.html",
        file_name=file_name,
        results=results,
        accuracy=round(accuracy, 2),
        false_negatives=round(false_negatives, 2),
        false_positives=round(false_positives, 2),
        time=(end-start)
    )
