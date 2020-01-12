import requests

#enable flask
#from flask import Flask
#app = Flask(__name__)
# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

#@app.route("/sentiment/<string:song>/<string:artist>")
def getMember(song,artist):
    return sentiment(song,artist)

# Instantiates a client
client = language.LanguageServiceClient.from_service_account_json(
        '../spotimaps-e9104cef02b9.json')

def sentiment(song,artist):
    #retrieve lyrics
    url = "https://api.musixmatch.com/ws/1.1/matcher.lyrics.get?q_track="+song+"&q_artist="+artist+"&apikey=5245cee9fb6c09e6a68af943ef79f34a"
    response = requests.get(url)
    
    try:
        text = response.json()["message"]["body"]["lyrics"]["lyrics_body"][:-53]
    except:
        return "(0.0, 0.0)"

    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(document=document).document_sentiment
    print(text)
    print("score:", sentiment.score, "magnitude", sentiment.magnitude)
    return str((sentiment.score, sentiment.magnitude))

if __name__ == "__main__":
    getMember("yellow submarine", "beatles")
