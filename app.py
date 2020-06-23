import json
from flask import Flask, render_template, request, get_template_attribute
from models.log_manager import LogManager
from models.sample_data import load_sample_data

LogManager.init()

LogManager.LogInfo('Starting MLM Demo Application...')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', sample_data=load_sample_data(), version='V1.0')

@app.route('/', methods=['POST'])
def post_requests():
    if 'text_query' in request.form:
        # TODO
        # text_query = request.form['text_query']
        # call model for results
        return 'Text Results'
    elif 'image_query' in request.form:
        # TODO
        # image_query = request.form['image_query']
        # call model for results
        return { 'coords': [3, 4], 'results': 'Image Results'}
    elif 'upload_query' in request.form:
        # TODO
        # upload image
        # read content
        # call model for results
        return 'Upload Results'
    elif 'get_summary' in request.form:
        label = request.form['get_summary']
        for data in load_sample_data():
            if label == data['label']:
                return data['summary']
        return ''

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')