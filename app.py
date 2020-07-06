import json
import random
from glob import glob
from models.image_upload import ImageUpload
from models.log_manager import LogManager
from models.mlm_inference import MLMInference
from models.news_articles_api import NewsArticlesApi
from flask import Flask, render_template, request, flash

LogManager.init()
LogManager.LogInfo('Starting MLM-Geo Application')

mlm_inference = MLMInference()
news_articles = NewsArticlesApi(api_key=open('ER_API_KEY').readline().rstrip())

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024 # allow max 1GB upload

@app.route('/')
def index():
    return render_template('index.html',
                        sample_images=glob('static/img/mlm/*'),
                        languages=['en', 'de', 'fr', 'it', 'es', 'pl', 'ro', 'nl', 'hu', 'pt'],
                        version='0.1')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' in request.files:
        # upload data
        file = request.files['file']
        if file.filename == '':
            return 'Uploaded image has no filename!', 400
        if file and ImageUpload.allowed_file(file.filename):
            query = ImageUpload.read_and_save_image(file.stream, file.filename)
            if query == '':
                return 'Could not read uploaded image. Please try again!', 400
        else:
            return 'Wrong file extension!', 400
    else:
        # sample data
        query = request.form['query'] if 'query' in request.form else ''

    # tasks, language and sample id
    tasks = request.form['tasks'] if 'tasks' in request.form else ['le', 'ir']
    lang = request.form['lang'] if 'lang' in request.form else 'en'
    sample_id = request.form['sample_id'] if 'sample_id' in request.form else None

    # mlm results
    results = mlm_inference.predict(query, tasks=tasks, lang=lang, sample_id=sample_id)

    # news articles
    for res_ir in results['ir']:
        res_ir['news_articles'] = news_articles.get_news_articles(res_ir['label'], lang)

    # reset news articles api
    news_articles.reset()

    # delete uploaded image
    ImageUpload.delete_upload_image(query)

    return results

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
