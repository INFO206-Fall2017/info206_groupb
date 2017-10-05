from Slackbot import intent_responder
from Slackbot.intent_responder import BARTQueryResponse, BusQueryResponse

class MessageFormatter:
  def format(self, response):
    if type(response) is BARTQueryResponse:
      return self.formatBARTResponse(response)
    elif type(response) is BusQueryResponse: 
      return self.formatBusResponse(response)
    else:
      return self.formatHelpResponse()
    pass

  def formatBARTResponse(self, response): 
    return {
        "attachments": [
            {
                "title": "Title",
                "pretext": "Pretext _supports_ mrkdwn",
                "text": "Testing *right now!*",
                "mrkdwn_in": [
                    "text",
                    "pretext"
                ]
            }
        ]
    }

  def formatBusResponse(self, response): 
    return {
        "attachments": [
            {
                "title": "Title",
                "pretext": "Pretext _supports_ mrkdwn",
                "text": "Testing *right now!*",
                "mrkdwn_in": [
                    "text",
                    "pretext"
                ]
            }
        ]
    }

  def formatHelpResponse(self):
    return {
        "attachments": [
            {
                "title": "Title",
                "pretext": "Pretext _supports_ mrkdwn",
                "text": "Testing *right now!*",
                "mrkdwn_in": [
                    "text",
                    "pretext"
                ]
            }
        ]
    }
