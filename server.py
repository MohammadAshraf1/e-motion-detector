from flask import Flask, request, render_template, url_for
from EmotionDetection import emotion_detector

app = Flask(
    __name__,
    template_folder='templates',
    static_folder='static'
)

@app.route("/")
def home():
    """
    Serve the HTML UI at the root URL.
    """
    return render_template("index.html")

@app.route("/emotionDetector")
def detect_emotion():
    """
    Accept ?textToAnalyze=... and return a formatted emotion response.
    """
    text_to_analyze = request.args.get('textToAnalyze', '')
    if not text_to_analyze:
        return "Error: 'textToAnalyze' query parameter is missing", 400

    emotions = emotion_detector(text_to_analyze)
    anger   = emotions['anger']
    disgust = emotions['disgust']
    fear    = emotions['fear']
    joy     = emotions['joy']
    sadness = emotions['sadness']
    dominant= emotions['dominant_emotion']

    response = (
        f"For the given statement, the system response is "
        f"'anger': {anger}, 'disgust': {disgust}, 'fear': {fear}, "
        f"'joy': {joy} and 'sadness': {sadness}. "
        f"The dominant emotion is {dominant}."
    )
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
