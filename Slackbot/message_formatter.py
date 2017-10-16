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
    list = []
    for r in response.routes:
        list.append(formatBARTResponseItem(r))

    return {
        "attachments": list
    }


  def formatBARTResponseItem(self, response): 

    # this will create a string of all the times
    # do this for every entry that is given
    timelist =""
    index = 0
    for time in response["departures"]:
        timelist += time

        # index is used here to not add a comma after the last numerical value
        index += 1

        if index != len(response["departures"]):
            timelist += ", "
    finaltimelist = timelist + " minutes"


    return {
                "title": response["destination"],
                "color": "#2ECC71",
                "pretext": "Latest BART times for {}".format(response["origin"]),
                "text": finaltimelist,
                "mrkdwn_in": [
                    "text",
                    "pretext"
                ]
            }
    


  # create the old formatBusResponse item below

  def formatBusResponse(self, response):
    list = []
    for r in response.routes:
        list.append(formatBusResponseItem(r))

    return {
        "attachments": list
    }



  def formatBusResponseItem(self, response): 
    # this will create a string of all the times
    # do this for every entry that is given
    timelist =""
    index = 0
    for time in response["departures"]:
        timelist += time
        index += 1
        if index != len(response["departures"]):
            timelist += ", "
    finaltimelist = timelist + " minutes"

    # check if the direction key exists. If not, then we show destination as the title instead
    if "direction" in response:
        directionordestination = response["direction"]
    else:
        directionordestination = response["destination"]

    # include code here that only diplays pretext once


    return {
                "title": directionordestination,
                "color": "#F4D03F",
                "pretext": "Latest Bus times for {}".format(response["origin"]),
                "text": finaltimelist,
                "mrkdwn_in": [
                    "text",
                    "pretext"
                ]
            }


  def formatHelpResponse(self):
    return {
        "attachments": [
            {
                "title": "A list of all stations can be found here.",
                "title_link": "https://www.bart.gov/stations",
                "color": "#E74C3C",
                "pretext": "I couldn't understand what you mean. Below is a link of all station names and the proper input formatting.",
                "text": "[Bart or Bus] + [Station Name] + [Line of station or direction]",
                "mrkdwn_in": [
                    "text",
                    "pretext"
                ]
            }
        ]
    }
