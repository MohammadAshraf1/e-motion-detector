import requests
# - requests is NOT built-in; it’s a third-party library used to make HTTP requests

import json
# - json is built-in; provides functions for parsing (and generating) JSON data

def emotion_detector(text_to_analyze):
    # Define the API endpoint URL
    # - string literal is built-in; this URL points to the Watson EmotionPredict service  
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'

    # Build the JSON payload as a Python dict
    # - dict literal is built-in; "raw_document" and "text" are keys expected by the API
    myobj = { "raw_document": { "text": text_to_analyze } }

    # Prepare the HTTP headers as a dict
    # - dict literal is built-in; the custom header tells the service which model to use
    header = { "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock" }

    # Send a POST request to the API
    # - requests.post() is NOT built-in; it’s provided by the requests library
    # - json=myobj tells requests to serialize myobj to a JSON request body
    # - headers=header attaches our model-selection header
    response = requests.post(url, json=myobj, headers=header)

    # Parse the raw JSON string from the response into a Python dict
    # - response.text is NOT built-in; it’s an attribute of the requests.Response object
    # - json.loads() is built-in to the json module; it converts JSON string to dict
    result = json.loads(response.text)

    # Extract the "emotion" dict from the first prediction entry
    # - result["emotionPredictions"] is a list (built-in type)
    # - [0] is list indexing (built-in)
    # - ["emotion"] is dict access (built-in)
    emotions = result["emotionPredictions"][0]["emotion"]

    # Determine which emotion has the highest score
    # - max() is built-in; key=emotions.get uses the dict .get() method (built-in)
    dominant_emotion = max(emotions, key=emotions.get)

    # Add the "dominant_emotion" key to the emotions dict
    # - dict assignment is built-in
    emotions["dominant_emotion"] = dominant_emotion

    # Return the final emotions dict (with scores and dominant emotion)
    return emotions
