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

    # this will create a string of all the times
    # do this for every entry that is given
    timelist =""
    index = 0
    for time in response.routes[0]["departures"]:
        timelist += time
        index += 1
        if index != len(response.routes[0]["departures"]):
            timelist += ", "
    finaltimelist = timelist + " minutes"

    return {
        "attachments": [
            {
                "title": response.routes[0]["destination"],
                "color": "#2ECC71",
                "pretext": "Latest BART times for {}".format(response.routes[0]["origin"]),
                "text": finaltimelist,
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
                "title": "[Bus Line]",
                "color": "#F4D03F",
                "pretext": "Latest bus times for [station name]",
                "text": "[time 1, time 2, time 3, minutes]",
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
                #"title": "Proper message formatting",
                "color": "#E74C3C",
                "pretext": "Proper message formatting is below",
                "text": "[Bart or Bus] + [Station Name] + [Line of station or direction]",
                "mrkdwn_in": [
                    "text",
                    "pretext"
                ]
            }
        ]
    }
