import os
import time
import json
from slackclient import SlackClient
from http.server import HTTPServer, BaseHTTPRequestHandler
from minimal_http_server import MinimalHTTPRequestHandler
from threading import Thread
from intent_recognizer import IntentRecognizer
from intent_responder import IntentResponder
from message_formatter import MessageFormatter

# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
PORT = int(os.environ.get("PORT", "8080"))

irec = IntentRecognizer()
ires = IntentResponder()
mf = MessageFormatter()

debug_on = False

def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines the intent and entities of the command.
        Respond to that intent or show a help message if no intent can be identified.
    """
    global debug_on
    if command == 'debug on':
        debug_on = True
    elif command == 'debug off':
        debug_on = False
    else:
        intent = irec.recognize(command)
        
        if debug_on:
            slack_client.api_call("chat.postMessage", 
                                channel=channel,
                                text="Found intent: " + json.dumps(intent.__dict__),
                                as_user=True)

        response = ires.respond_to_intent(intent)

        if debug_on:
            slack_client.api_call("chat.postMessage", 
                                channel=channel,
                                text="Response: " + json.dumps(response.__dict__),
                                as_user=True)

        slack_response = mf.format(response)
        if 'attachments' in slack_response:
            slack_client.api_call("chat.postMessage", 
                                    channel=channel,
                                    attachments=slack_response["attachments"],
                                    as_user=True)
        elif 'text' in slack_response:
            slack_client.api_call("chat.postMessage", 
                                    channel=channel,
                                    text=slack_response["text"],
                                    as_user=True)


def parse_slack_output(slack_rtm_output):
    """
        Parses the message from RTM and returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None

def runHttp(server_class=HTTPServer, handler_class=MinimalHTTPRequestHandler):
    """
        Start a minimal HTTP server that serves a blank page to comply with Heroku's hosting requirements.
    """
    server_address = ('', PORT)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    print("starting HTTP Server")
    thread = Thread(target = runHttp)
    thread.start()
    if slack_client.rtm_connect():
        print("RTM connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")

