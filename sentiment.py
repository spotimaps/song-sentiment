# Imports the Google Cloud client library
from flask import Flask
app = Flask(__name__)

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import requests

@app.route("/sentiment/<string:song>/")
def getMember(song):
    return sentiment(song)

# Instantiates a client
client = language.LanguageServiceClient.from_service_account_json(
        'spotimap_key.json')

def sentiment(song):
    #get lyrics here somehow
    text = u'Hello, world!' ###some function to get lyrics
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(document=document).document_sentiment
    return (sentiment.score, sentiment.magnitude)


