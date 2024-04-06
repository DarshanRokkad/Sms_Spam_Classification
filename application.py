from flask import Flask, render_template, request
from src.pipeline.prediction_pipeline import PredictionPipeline

application = Flask(__name__)
app = application

@app.route('/', methods = ['GET', 'POST'])
def home_page():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        text = request.form['text']
        prediction_pipeline = PredictionPipeline()
        result = prediction_pipeline.predict(text)
        return render_template('home.html', prediction = result)

if __name__ == '__main__':
    application.run()