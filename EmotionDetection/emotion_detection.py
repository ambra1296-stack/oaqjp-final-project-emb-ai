import requests  # Import the requests library to handle HTTP requests
import json

def emotion_detector(text_to_analyze):  #
    # Define a function named sentiment_analyzer that takes a string input (text_to_analyse)
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'  # URL of the emotion detect service
    myobj = { "raw_document": { "text": text_to_analyze } }  # Create a dictionary with the text to be analyzed
    header = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}  # Set the headers required for the API request
    response = requests.post(url, json = myobj, headers=header)  # Send a POST request to the API with the text and headers
    # Parsing the JSON response from the API
    formatted_response = json.loads(response.text)
    #If the response status code is 200, extract emotions and score from the response
    if response.status_code == 200:
        # Extracting emotion label and score from the response
        # Navigate the nested structure to find the primary emotion scores
        # The scores are located within 'emotionPredictions' (a list), 
        # then the first item [0], then the 'emotion' dictionary.
        emotion_scores = formatted_response['emotionPredictions'][0]['emotion']
        # Extract individual scores
        anger_score = emotion_scores['anger']
        disgust_score = emotion_scores['disgust']
        fear_score = emotion_scores['fear']
        joy_score = emotion_scores['joy']
        sadness_score = emotion_scores['sadness']
        # Determine the dominant emotion
        # We use max() with a lambda function (key=emotion_scores.get) to find 
        # the emotion with the highest score in the dictionary.
        dominant_emotion = max(emotion_scores, key=emotion_scores.get)
        #Format the output dictionary as requested
        output = {
            'anger': anger_score,
            'disgust': disgust_score,
            'fear': fear_score,
            'joy': joy_score,
            'sadness': sadness_score,
            'dominant_emotion': dominant_emotion
        }
    # If the response status code is 400, set label and score to None
    elif response.status_code == 400:
        anger_score = None
        disgust_score = None
        fear_score = None
        joy_score = None
        sadness_score = None
        dominant_emotion = None
    # Returning a dictionary containing emotion analysis results
    return {
    'anger': anger_score,
    'disgust': disgust_score,
    'fear': fear_score,
    'joy': joy_score,
    'sadness': sadness_score,
    'dominant_emotion': dominant_emotion}