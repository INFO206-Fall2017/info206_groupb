from Slackbot import intent_responder
from Slackbot.intent_responder import BARTQueryResponse, BusQueryResponse

class MessageFormatter:
  def format(self, response, index):
    if type(response) is BARTQueryResponse:
      return self.formatBARTResponse(response, index)
    elif type(response) is BusQueryResponse: 
      return self.formatBusResponse(response, index)
    else:
      return self.formatHelpResponse()
    pass

  def formatBARTResponse(self, response, trainindex): 

    # this will create a string of all the times
    # do this for every entry that is given
    timelist =""
    index = 0
    for time in response.routes[trainindex]["departures"]:
        timelist += time
        index += 1
        if index != len(response.routes[trainindex]["departures"]):
            timelist += ", "
    finaltimelist = timelist + " minutes"

    return {
        "attachments": [
            {
                "title": response.routes[trainindex]["destination"],
                "color": "#2ECC71",
                "pretext": "Latest BART times for {}".format(response.routes[trainindex]["origin"]),
                "text": finaltimelist,
                "mrkdwn_in": [
                    "text",
                    "pretext"
                ]
            }
        ]
    }

  def formatBusResponse(self, response, busindex): 
    # this will create a string of all the times
    # do this for every entry that is given
    timelist =""
    index = 0
    for time in response.routes[busindex]["departures"]:
        timelist += time
        index += 1
        if index != len(response.routes[busindex]["departures"]):
            timelist += ", "
    finaltimelist = timelist + " minutes"

    return {
        "attachments": [
            {
                "title": "[Bus Destination or Direction]",
                "color": "#F4D03F",
                "pretext": "Latest Bus times for {}".format(response.routes[busindex]["origin"]),
                "text": finaltimelist,
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
