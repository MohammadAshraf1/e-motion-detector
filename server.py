"""
Server module for Emotion Detection application.
"""

from flask import Flask, request, render_template
# - Flask, request, render_template are from the Flask library (not built-in)

from EmotionDetection import emotion_detector
# - emotion_detector is our function from the custom EmotionDetection package

# Create Flask app, specifying folders for HTML templates and static files
app = Flask(
    __name__,
    template_folder='templates',  # built-in str used to point to templates/
    static_folder='static'        # built-in str used to point to static/
)

@app.route("/", methods=["GET"])
def home() -> str:
    """
    Serve the main HTML UI page.
    """
    # render_template is from Flask; loads templates/index.html and returns HTML
    return render_template("index.html")

@app.route("/emotionDetector", methods=["GET"])
def detect_emotion() -> str:
    """
    Handle emotion detection requests.
    """
    # request.args.get is from Flask; retrieves query parameter or defaults to ""
    text_to_analyze = request.args.get("textToAnalyze", "")
    if not text_to_analyze:
        # returning tuple (message, status) triggers HTTP 400 Bad Request
        return "Error: 'textToAnalyze' query parameter is missing", 400

    # Call our package’s function; returns a dict of emotion scores
    emotions = emotion_detector(text_to_analyze)

    # If dominant_emotion is None, treat as invalid input
    if emotions.get("dominant_emotion") is None:
        return "Invalid text! Please try again!", 400

    # Extract individual scores from the dict (built-in dict access)
    anger = emotions["anger"]
    disgust = emotions["disgust"]
    fear = emotions["fear"]
    joy = emotions["joy"]
    sadness = emotions["sadness"]
    dominant = emotions["dominant_emotion"]

    # Build a formatted response using f-strings (built-in feature)
    response = (
        f"For the given statement, the system response is "
        f"'anger': {anger}, 'disgust': {disgust}, 'fear': {fear}, "
        f"'joy': {joy} and 'sadness': {sadness}. "
        f"The dominant emotion is {dominant}."
    )
    return response

if __name__ == "__main__":
    # app.run is from Flask; starts the development server on port 5000
    app.run(host="0.0.0.0", port=5000)
