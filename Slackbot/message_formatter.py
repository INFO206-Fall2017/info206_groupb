from Slackbot import intent_responder
from Slackbot.intent_responder import BARTQueryResponse as BARTQueryResponse
from Slackbot.intent_responder import BusQueryResponse as BusQueryResponse

# set up 4 colors to cycle through for each "time"
colorlist = ["#F4D03F", "#3498DB", "#2ECC71", "#E74C3C"]

class MessageFormatter:
  def format(self, response):
    if type(response).__name__ == 'BARTQueryResponse':
      print("bart object instance")
      return self.formatBARTResponse(response)
    elif type(response).__name__ == 'BusQueryResponse': 
      print("bus ofject instance")
      return self.formatBusResponse(response)
    else:
      return self.formatHelpResponse()
    pass

  def formatBARTResponse(self, response):
    list = []
    colorcounter = 0
    for r in response.routes:
        list.append(self.formatBARTResponseItem(r, colorcounter))
        colorcounter += 1

    return {
        "attachments": list
    }


  def formatBARTResponseItem(self, response, colorcounter): 

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
                "color": colorlist[colorcounter%4],
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
    colorcounter = 0
    for r in response.routes:
        list.append(self.formatBusResponseItem(r, colorcounter))
        colorcounter += 1

    return {
        "attachments": list
    }



  def formatBusResponseItem(self, response, colorcounter): 
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
                "color": colorlist[colorcounter%4],
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
