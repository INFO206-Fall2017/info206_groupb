from Slackbot import intent_responder
from Slackbot.intent_responder import BARTQueryResponse as BARTQueryResponse
from Slackbot.intent_responder import BusQueryResponse as BusQueryResponse
from Slackbot.intent_responder import NamesNotFoundResponse as NamesNotFoundResponse


# Set up 5 colors to cycle through for each train/bus "time"
colorlist = ["#F4D03F", "#3498DB", "#2ECC71", "#E74C3C", "#85C1E9"]

class MessageFormatter:
  def format(self, response):
    """
    Checks the type of each response. Depending on the type, a different formatresponse function will be called.
    Each different formatresponse function will have specific formatting guidelines.
    """

    # Calls the proper formatting function for each type
    if type(response).__name__ == 'BARTQueryResponse':
      return self.formatBARTResponse(response)
    elif type(response).__name__ == 'BusQueryResponse': 
      return self.formatBusResponse(response)
    elif type(response).__name__ == 'NamesNotFoundResponse': 
      return self.formatNamesNotFoundResponse(response)
    elif type(response).__name__ == 'NoDeparturesResponse':
      return self.formatNoDeparturesResponse(response)
    else:
      return self.formatHelpResponse()
    pass


  def formatBARTResponse(self, response):
    """
    This function is mainly used for final adjustments to the attachment formatting.
    It calls the primary formatting function that makes the main attachment changes. 
    This function calls formatBARTresponseItem for every dictionary in response and 
    appends the changes dictionary values with the correct attachments to an empty list
    and then returns it.
    """

    # Create empty list to return later on
    list = []

    # Allows the first item's "time" to be the first color in the color list.
    colorcounter = 0

    # Calls the primary formatting function for every dictionary in response
    for r in response.routes:
        item = self.formatBARTResponseItem(r, colorcounter)

        # If there is more than one dictionary, then delete the pretext key so it doesn't repeat in the slack channel
        if colorcounter > 0:
            del item["pretext"]

        # If there is a train that is leaving then display this gif in the slack message from the bot
        if "Leaving" in item["text"]:
            item["image_url"] = "https://media.giphy.com/media/oEoFTNBIsthzG/giphy.gif"

        # Append each changed dictionary to be returned later
        list.append(item)

        # Increase the color count so the color attachment changes 
        colorcounter += 1

    # Return the final list of properly formatted attachment dictionaries
    return {
        "attachments": list
    }


  def formatBARTResponseItem(self, response, colorcounter): 
    """
    This is the main formatting function where the title, color, pretext, and times are
    inserted in the new properly formatted dictionary for trains. This dictionary is then returned.
    """

    # Create an empty string that will be filled with departure times
    timelist =""

    # Set counter to 0
    index = 0

    # For each time, add it to the empty list
    for time in response["departures"]:
        timelist += time
        
        # Index is used here to not add a comma after the last numerical value in the string for times
        index += 1
        if index != len(response["departures"]):
            timelist += ", "

    finaltimelist = timelist + " minutes"    

    # Return the properly formatted dictionary
    return {
                "title": response["destination"],
                "color": colorlist[colorcounter%5],
                "pretext": "Latest BART times for {}".format(response["origin"]),
                "text": finaltimelist,
                "mrkdwn_in": [
                    "text",
                    "pretext"
                ]
            }
    




  def formatBusResponse(self, response):
    """
    This function is mainly used for final adjustments to the attachment formatting.
    It calls the primary formatting function that makes the main attachment changes. 
    This function calls formatBUSresponseItem for every dictionary in response and 
    appends the changes dictionary values with the correct attachments to an empty list
    and then returns it.
    """

    # Create empty list to return later on
    list = []

    # Allows the first item's "time" to be the first color in the color list.
    colorcounter = 0
    for r in response.routes:
        item = self.formatBusResponseItem(r, colorcounter)

        # If there is more than one dictionary, then delete the pretext key so it doesn't repeat in the slack channel
        if colorcounter > 0:
            del item["pretext"]

        # If there is a bus that is leaving then display this gif in the slack message from the bot
        if "Leaving" in item["text"]:
            item["image_url"] = "https://media.giphy.com/media/oEoFTNBIsthzG/giphy.gif"
        
        # Append each changed dictionary to be returned later
        list.append(item)

        # Increase the color count so the color attachment changes
        colorcounter += 1

    # Return the final list of properly formatted attachment dictionaries
    return {
        "attachments": list
    }



  def formatBusResponseItem(self, response, colorcounter): 
    """
    This is the main formatting function where the title, color, pretext, and times are
    inserted in the new properly formatted dictionary for buses. This dictionary is then returned.
    """

    # Create an empty string that will be filled with departure times
    timelist =""

    # Set counter to 0
    index = 0

    # For each time, add it to the empty list
    for time in response["departures"]:
        timelist += time

        # Index is used here to not add a comma after the last numerical value in the string for times
        index += 1
        if index != len(response["departures"]):
            timelist += ", "
    finaltimelist = timelist + " minutes"

    # Check if the direction key exists. If not, then we show destination as the title instead
    if "direction" in response:
        directionordestination = response["direction"]
    else:
        directionordestination = response["destination"]

    route_part = ""
    route_str = response.get("route_name", None)
    if route_str:
        route_part = "on " + route_str
    # Return the properly formatted dictionary
    return {
                "title": directionordestination,
                "color": colorlist[colorcounter%5],
                "pretext": "Latest Bus times for {} {}".format(response["origin"],route_part),
                "text": finaltimelist,
                "mrkdwn_in": [
                    "text",
                    "pretext"
                ]
            }

  def formatNamesNotFoundResponse(self, response):
    """
    This function is used when the format is correct but the station name is incorrect.
    It will tell the user that it doesn't recognize the name.
    """

    # Create an empty list names
    names = []

    # Goes through each name and appends the name value to the name list
    for n in response.names:
        names.append('"' + n["name"] + '"')

    # After each element, return attachment which specifies that it doesn't know these names
    return {
        "text": "I don't know what's " + ','.join(names)
    }

  def formatNoDeparturesResponse(self, response):
    """
    This function is used when the format is correct, but there are no more
    trains or buses departing from that station at the current time.
    """

    # Returns value that tells user there are no departures.
    return {
      "text": "There's currently no departures on that route from that station."
    }

  def formatHelpResponse(self):
    """
    This function is called when the user inputs the incorrect format.
    As a response, we will show the user the correct format they will follow,
    links to both bart and bus station names, and a gif to brighten the mood.
    """

    # Returns attachments with correct format, links, and gif
    return {
        "attachments": [
            {
                "title": "Proper input formatting is shown below: ",
                "color": "#E74C3C",
                "pretext": "I couldn't understand what you mean. Below is a link of all station names and the proper input formatting.",
                "text": "[Bart or Bus] + [Station Name] + [Line of station or direction]",
                "fields": [
                    {
                        "title":"List of all BART stations here: ",
                        "value": "https://www.bart.gov/stations"
                    },
                    {
                        "title":"List of all Bus stations here: ",
                        "value": "http://www.nextbus.com/#!/actransit/B/B_61_0/1410350/1014970"
                    }
                ],
                "image_url": "https://media.giphy.com/media/kLpkCMqucdva/giphy.gif"
                
            }
        ]
    }
