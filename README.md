# Repository for final project
# Emotion Detection Application

This project demonstrates how to build a simple sentiment/emotion detection web application using Flask and IBM Watson's Embeddable AI Emotion Service. The application:

* Exposes a web UI (HTML/JS) where users input text.
* Sends the text to IBM Watson’s Embeddable EmotionPredict API.
* Parses and displays emotion scores (anger, disgust, fear, joy, sadness) and the dominant emotion.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Project Structure](#project-structure)
4. [How Sentiment/Emotion Analysis Works](#how-sentimentemotion-analysis-works)
5. [Integrating IBM Watson Embeddable AI](#integrating-ibm-watson-embeddable-ai)
6. [Code Walkthrough](#code-walkthrough)

   * [emotion\_detection.py](#emotion_detectionpy)
   * [server.py](#serverpy)
   * [Front-end (index.html & mywebscript.js)](#front-end-indexhtml--mywebscriptjs)
7. [Running the Application](#running-the-application)
8. [Testing & Error Handling](#testing--error-handling)
9. [Troubleshooting](#troubleshooting)

---

## Prerequisites

* Python 3.7+
* `pip` package manager
* Internet access (for calling the Watson service)
* An IBM Cloud account with access to the Embeddable AI Emotion Service or the public test endpoint used here.

## Installation

1. **Clone the repo** into a folder named `final_project`:

   ```bash
   git clone https://github.com/<your-username>/oaqjp-final-project-emb-ai.git final_project
   cd final_project
   ```
2. **Install dependencies**:

   ```bash
   pip install flask requests
   ```

## Project Structure

```
final_project/
├── EmotionDetection/      # Python package with emotion_detector()
│   ├── __init__.py        # Exports emotion_detector
│   └── emotion_detection.py
├── static/                # Static assets (JS)
│   └── mywebscript.js
├── templates/             # HTML templates
│   └── index.html
├── server.py              # Flask application entrypoint
└── README.md              # This file
```

## How Sentiment/Emotion Analysis Works

1. **User Input**: Text is entered in the front-end form.
2. **API Call**: The back-end sends an HTTP POST to Watson’s `EmotionPredict` service with JSON payload:

   ```json
   { "raw_document": { "text": "I love my life" } }
   ```
3. **Model Inference**: Watson returns emotion scores:

   ```json
   {
     "emotionPredictions": [
       {
         "emotion": { "anger":0.006, "joy":0.968, ... }
       }
     ]
   }
   ```
4. **Parse & Display**: Back-end picks the highest score as the dominant emotion and front-end shows all scores.

## Integrating IBM Watson Embeddable AI

We use Watson’s Embeddable EmotionPredict endpoint. Key steps:

1. **Endpoint URL**:

   ```python
   url = (
     'https://sn-watson-emotion.labs.skills.network/v1/' +
     'watson.runtime.nlp.v1/NlpService/EmotionPredict'
   )
   ```
2. **Headers**: Specify the model ID:

   ```python
   headers = {
     'grpc-metadata-mm-model-id':
       'emotion_aggregated-workflow_lang_en_stock'
   }
   ```
3. **Payload**: Wrap text in `raw_document`:

   ```python
   payload = { 'raw_document': { 'text': text_to_analyze } }
   ```
4. **HTTP Request**: Using `requests.post(url, json=payload, headers=headers)`.

---

## Code Walkthrough

### emotion\_detection.py

```python
import requests
import json

def emotion_detector(text_to_analyze):
    # Build request
    url = 'https://sn-watson-emotion.labs.skills.network/.../EmotionPredict'
    payload = { 'raw_document': { 'text': text_to_analyze } }
    headers = { 'grpc-metadata-mm-model-id':
                'emotion_aggregated-workflow_lang_en_stock' }

    # Call API
    response = requests.post(url, json=payload, headers=headers)

    # Error handling: blank input returns None-filled dict
    if response.status_code == 400:
        return { k: None for k in
                 ['anger','disgust','fear','joy','sadness'] }

    # Parse JSON
    result = json.loads(response.text)
    emotions = result['emotionPredictions'][0]['emotion']

    # Determine dominant emotion
    dominant = max(emotions, key=emotions.get)
    emotions['dominant_emotion'] = dominant
    return emotions
```

**Explanation**:

* `requests` (third-party) sends HTTP calls.
* `json.loads` (built-in) parses the JSON string.
* `max(dict, key=...)` picks the highest-score emotion.

### server.py

```python
from flask import Flask, request, render_template
from EmotionDetection import emotion_detector

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/emotionDetector')
def detect_emotion():
    text = request.args.get('textToAnalyze','')
    if not text:
        return "Invalid text! Please try again!", 400
    
    emotions = emotion_detector(text)
    if emotions.get('dominant_emotion') is None:
        return "Invalid text! Please try again!", 400

    # Format output
    resp = (
      f"For the given statement, the system response is "
      f"'anger': {emotions['anger']}, ... "
      f"dominant emotion is {emotions['dominant_emotion']}"
    )
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

**Explanation**:

* Flask’s `@app.route` binds URLs to functions.
* `render_template` (Flask) serves `index.html`.
* Query parameters accessed via `request.args.get`.

### Front-end (index.html & mywebscript.js)

```html
<!-- index.html -->
<input id="textToAnalyze" ...>
<button onclick="RunSentimentAnalysis()">Run</button>
<div id="system_response"></div>
<script src="{{ url_for('static', filename='mywebscript.js') }}"></script>
```

```js
// mywebscript.js
function RunSentimentAnalysis(){
  let text = document.getElementById('textToAnalyze').value;
  fetch('/emotionDetector?textToAnalyze='+encodeURIComponent(text))
    .then(r => r.ok ? r.text() : r.text().then(t=>{throw t}))
    .then(data=>document.getElementById('system_response').innerText=data)
    .catch(err=>document.getElementById('system_response').innerText=err);
}
```

**Explanation**:

* JS `fetch` sends GET to `/emotionDetector`.
* On success, display response; on error, display error text.

---

## Running the Application

1. Start the server:

   ```bash
   python3 server.py
   ```
2. Visit:

   ```
   http://127.0.0.1:5000/
   ```
3. Enter text and click **Run Sentiment Analysis**.

## Testing & Error Handling

* Blank input returns **Invalid text! Please try again!**
* Valid input shows emotion scores and dominant emotion.

---

## Troubleshooting

* **Port in use**: kill old process (`fuser -k 5000/tcp`) or change port.
* **Template not found**: ensure `templates/index.html` exists and Flask’s `template_folder` is correct.

---

© 2025 Your Name. All rights reserved.
