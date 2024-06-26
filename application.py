from flask import Flask, render_template, request, jsonify
from src.pipeline.prediction_pipeline import PredictionPipeline


application = Flask(__name__)
app = application

@app.route('/')
def home_page():
    return render_template('home.html')
    
@app.route('/detect', methods = ['GET', 'POST'])
def form_page():
    if request.method == 'GET':
        return render_template('form.html')
    else:
        text = request.form['text']
        prediction_pipeline = PredictionPipeline()
        result = prediction_pipeline.predict(text)
        return render_template('result.html', prediction = result)

# api testing
@app.route('/detect_api', methods = ['GET', 'POST'])
def api_testing():
    if request.method == 'GET':
        return 'Nothing'
    else:
        text = request.json['text']
        prediction_pipeline = PredictionPipeline()
        result = prediction_pipeline.predict(text)
        return jsonify(result)


if __name__ == '__main__':
    application.run(host = '0.0.0.0', port = 5000, debug = True)