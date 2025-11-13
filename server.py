"""
Emotion Detector Flask Application.

This application provides a simple API endpoint '/emotionDetector'
to analyze text input and determine the emotional content using an external
emotion detection module (EmotionDetection.emotion_detector). It also serves 
a homepage at the root '/'.
"""
from flask import Flask, render_template, request
# NOTE: The 'EmotionDetection' module is assumed to be available
from EmotionDetection.emotion_detection import emotion_detector
app = Flask("Emotion Detector")

@app.route("/emotionDetector")
def emot_detector():
    """
    Analyzes the text provided in the 'textToAnalyze' query parameter.

    This function retrieves the text, passes it to the emotion detection module,
    and formats the resulting scores (anger, disgust, fear, joy, sadness) 
    along with the dominant emotion into a human-readable string.

    Query Params:
        textToAnalyze (str): The text string to be analyzed.

    Returns:
        str: A formatted string displaying all emotion scores and the dominant emotion,
             or an "Invalid input" message if the input is missing or the detector fails.
    """
    # Retrieve the text to analyze from the request arguments
    text_to_analyze = request.args.get('textToAnalyze')

    # Check for empty input before proceeding
    if text_to_analyze is None or text_to_analyze.strip() == "":
        return "Invalid input! Text to analyze is missing or empty."

    # Pass the text to the emotion detector function and store the response
    response = emotion_detector(text_to_analyze)

    # Extract the emotion from the response
    anger_score = response['anger']
    disgust_score = response['disgust']
    fear_score = response['fear']
    joy_score = response['joy']
    sadness_score = response['sadness']
    dominant_emotion = response['dominant_emotion']

    # R1705 Fix: Removed unnecessary 'else' block
    if dominant_emotion is None:
        return "Invalid input! Try again."

    # C0301/C0209 Fix: Converted to f-string and wrapped lines
    return (
        f"For the given statement, the system response is 'anger': {anger_score}, "
        f"'disgust':{disgust_score}, 'fear': {fear_score}, 'joy': {joy_score} "
        f"and 'sadness':{sadness_score}. The dominant emotion is {dominant_emotion}."
    )

@app.route("/")
def render_index_page():
    """
    Renders the default homepage.

    This function is mapped to the root URL and simply serves the 'index.html' template.

    Returns:
        str: The rendered HTML content of the index page.
    """
    return render_template('index.html')

if __name__ == "__main__":
    # Runs the application on all available network interfaces on port 5000
    app.run(host="0.0.0.0", port=5000)
