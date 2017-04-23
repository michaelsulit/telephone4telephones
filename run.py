from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse, Message
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client
import requests



app = Flask(__name__)
last_url = []
PhoneNumbers=[]

account_sid = "AC63f63bab49ffb5b3df2dd3866c38e1b2"
auth_token = "0bf99c196c9c2f8c6568d0c1948cb65a"
client = Client(account_sid, auth_token)



@app.route("/text", methods=['GET', 'POST'])
def text_receive():
    """Respond to incoming calls with a simple text message."""

    from_number = request.values.get('From', None)
    text_body = request.values.get('Body', None)
    if(from_number == "+19739074375" and text_body == "go"):
        begin_calls()
    if from_number:
        PhoneNumbers.append(from_number)
    print PhoneNumbers


    #post to thingspace
    #https://thingspace.io/dweet/for/my-thing-name?key=value

    url = 'https://thingspace.io/dweet/for/telephone4telephones' # Set destination URL here
    post_fields = {'Number of Phones': len(PhoneNumbers),'New Phone': from_number}     # Set POST fields here

    r = requests.post(url, post_fields)
    #urllib2.urlopen("https://thingspace.io/dweet/for/my-thing-name?key=value").read()


    resp = MessagingResponse().message(from_number)
    return str(resp)

@app.route("/next-call", methods=['GET', 'POST'])
def next_call():
    resp = VoiceResponse()
    print "--"
    print last_url
    print "--"
    if not last_url:
        resp.say("Welcome to today's game of telephone. At the beep, record a phrase to get passed around.")
    else:
        resp.say("Welcome to today's game of telephone. At the beep, try to repeat the following phrase as best as you can.")
        resp.play(last_url.pop())

    resp.record(maxLength="5", action="/handle-recording")
    return str(resp)

@app.route("/last-call", methods=['GET', 'POST'])
def last_call():
    resp = VoiceResponse()
    resp.say("Thanks for playing telephone. Here is the final phrase that resulted.")
    resp.play(last_url.pop())
    return str(resp)

@app.route("/handle-recording", methods=['GET', 'POST'])
def handle_recording():
    """Play back the caller's recording."""

    #recording_url = request.values.get("RecordingUrl", None)
    resp = VoiceResponse()


    last_url.append(request.values.get("RecordingUrl", None))
    if PhoneNumbers:
        call = client.api.account.calls.create(to=PhoneNumbers.pop(),  # Any phone number
            from_="+12013971017", # Must be a valid Twilio number
            url="http://f81a966a.ngrok.io/next-call")
    '''
    else:
        call = client.api.account.calls.create(to=PhoneNumbers.pop(),  # Any phone number
            from_="+12013971017", # Must be a valid Twilio number
            url="http://f81a966a.ngrok.io/last-call")'''


    resp.say("Goodbye.")
    print last_url
    return str(resp)

def begin_calls():

    PhoneNumbers.reverse()

    if PhoneNumbers:
        call = client.api.account.calls.create(to=PhoneNumbers.pop(),  # Any phone number
            from_="+12013971017", # Must be a valid Twilio number
            url="http://f81a966a.ngrok.io/next-call")


if __name__ == "__main__":
    app.run(debug=True)
