import requests

#enable flask
from flask import Flask
app = Flask(__name__)
# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

@app.route("/sentiment/<string:song>/<string:artist>")
def getMember(song,artist):
    return color_from(song,artist)

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

    print("score:", sentiment.score, "magnitude", sentiment.magnitude)
    return (sentiment.score, sentiment.magnitude)

def color_from(song, artist):
    color = [142,93,42] #in between

    happy = [29,186,84] #green
    sad = [255, 0, 0] #red
    
    sentiments = sentiment(song, artist)
    product = sentiments[0] * sentiments[1]

    if product > 0.3:
        color = happy

    elif product < 0.3:
        color = sad
    else:
        color[0] = color[0] + ((happy[0]-sad[0])/0.6) * product
        color[1] = color[1] + ((happy[1]-sad[1])/0.6) * product
        color[2] = color[2] + ((happy[2]-sad[2])/0.6) * product

    return 'rgb(' + str(red) +','+ str(green)+','+ str(blue)+')'

if __name__ == "__main__":
    app.run()
