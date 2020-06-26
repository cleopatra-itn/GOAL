import json
from flask import Flask, render_template, request, get_template_attribute
from models.log_manager import LogManager
from models.sample_data import load_sample_data
from models.inference import get_results

LogManager.init()

LogManager.LogInfo('Starting MLM Demo Application...')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', sample_data=load_sample_data(), version='0.1')

@app.route('/', methods=['POST'])
def post_requests():
    query = request.form['query']
    lang = request.form['lang']
    return get_results(query, lang)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')