# info206_groupb
Project:
For our project, we plan to create a slack bot that users can use to obtain real time data regarding bus and BART arrival and departure times. If time permits, we will add more features to the bot.

## Team Members:
* Devin Huang
* Anu Pandey
* Dylan Fox
* Soravis Prakkamakul

## Requirements

* Python >= 3.6
* Access to Wit.ai
* Access to Slack API

## Getting Started

To get started, use the following command from the project root directory

``` sh
pip install pipenv # Install Pipenv if you do not have one
pipenv run python3 Slackbot/slackbot.py

export BOT_ID=YOUR_BOT_ID
export SLACK_BOT_TOKEN=YOUR_SLACK_BOT_TOKEN
export WIT_AI_ACCESS_TOKEN=YOUR_WIT_AI_ACCESS_TOKEN
python Slackbot/slackbot.py
```
## Production Deployment

This project supports hosting on heroku through Procfile and Pipfile. To run on heroku, follow these steps

``` sh
heroku create
heroku config:set BOT_ID=YOUR_BOT_ID
heroku config:set SLACK_BOT_TOKEN=YOUR_SLACK_BOT_TOKEN
heroku config:set WIT_AI_ACCESS_TOKEN=YOUR_WIT_AI_ACCESS_TOKEN
git push heroku master
```
## BART 

https://api.bart.gov/docs/overview/index.aspx / BART API gives access to information about BART services and station data available on the BART website. The requests are sent using the requests library that allows sending HTTP/1.1 requests. The requests generates a json output that  returns a dictionary which comprises of a list of stations - which is in further comprised of more dictionaries
        {[{},{},{},{}],[{},{},{},{}],[{},{},{},{}],[{},{},{},{}]}


The code gives output for these 3 scenarios

CASE1 ) User can input name of station( “Departing from” station ) and BART line. 
Input format:  BART    Station name       BART line
This input search will display the time schedule of next BART available from the input BART station for the input BART line (only). For example the input BART Downtown Berkeley Richmond would only display the time schedule of the next BART train from Downtown Berkeley station towards Richmond Line.

CASER 2) Users can only input the name of station ( “Departing from” station) without specifying a BART  line
Input format:  BART    Station name
This input search will display a list of time schedules for all BART line from the input BART
station. For example the input BART Richmond will provide the user the time schedules for the next available BART for all lines such as Richmond, Daly City, Warm Springs/South Fremont, Fremont, Pleasanton/Dublin, Pittsburg/Bay Point.

Option 3) Users can input name of 2 stations ( “Departing from”  and "arriving at" station)
Input format:  BART    Station name1      Station name2
This input search will display a the time schedule for a BART that can help users reach from BART station1 to BART station2.
For example the input BART Richmond   Fremont will provide the user the time schedules for the next available BART from Richmond to Fremont.

The only mandatory input required from the user is the name of departing from station

If the bart.py is run as a separate script. The script requires the user to input the "departing from" station(mandatory)
, bart line , and "arriving at" station.
The BART folder has a file named that test_bart.py has a unit test to test fucntions (from bart.py) that yield a static output.


'''

## NextBus

### NextBus XML Feed

[NextBus](https://www.nextbus.com/) offers an XML feed through which applications can request bus information. The full documentation is [here](https://www.nextbus.com/xmlFeedDocs/NextBusXMLFeed.pdf) , but we used the commands below. We also used **urllib.request** to get the URLs, and **xml.etree.ElementTree** to parse the returned XML.

The inputs from the user are a route (mandatory), stop (mandatory), and destination (optional). E.g. 'Telegraph and 40th 6 Foothill Square'.

Our NextBus.py code returns a dictionary with keys of destination names and values of a list of upcoming departure times for that destination, as well as booleans indicating whether any routes or stops were returned that we use in handling errors.




#### Agency List

*Input: None*

*Output: List of agency tags*

Obtains a list of available transit agencies. Currently we've hardcoded it to use actransit, but with minimum modifications it could be used for any of NextBus's affiliate transit systems.

#### Route List

*Input: Agency tag*

*Output: List of routes for that agency*

We used this command to create a dictionary of routes that we could compare the user's route request against.

#### Route Config

*Input: Agency, Route*

*Output: List of stops for a given route*

We used this to create a dictionary of stops that we could compare the user's stop request against. Because NextBus requires a route for this command if more than 100 routes would be returned otherwise (and AC Transit has >150 routes), we require the user to enter a route, not just a stop.

#### Prediction Request

*Input: Agency, Route, Stop*

*Output: List of departure times for buses heading out from this stop; one list for each route destination.*

Finally, we use this command to generate the key information our users are after: upcoming departure times. If the user provided a destination, we filter the results to show only that destination. 

## Slack Message Formatting

### Attachment Formatting Functions

message_formatter.py is used to format resulting data from Nextbus and Bart depending on the type of response. The format() function within this script will call 5 different formatting functions depending on the type. These five types are:

* formatBARTResponse()
* formatBusResponse()
* formatNamesNotFoundResponse()
* formatNoDeparturesResponse()
* formatHelpResponse()

BARTQueryResponse and BusQueryResponse types will call their own individual functions in which the values in the respective dictionaries will be inserted into Slack messaging attachments. This converted attachment will then be posted on Slack where departing times will be listed. 

NamesNotFoundResponse types will call a function that returns a formatted message telling the user that it doesn't know what the user typed in. This will be called when an incorrect station name is given.

NoDepartureResponse types will call a function that returns a formatted message in which it tells the user that there are currently no departures on that route. This will be called when there are no longer any departures for that station.

Everything else will call the formatHelpResponse function that formats a message telling the user what the correct format will be as well as links to station names of both Bart and NextBus. This will be called with the user does not follow the proper format for inputs.

## Testing

### Run all testcases at once
``` sh
py.test
```

### Run Individual Tests
```
py.test Tests/test_intent_recognizer.py -s
py.test Tests/test_intent_responder.py -s
py.test Tests/test_message_formatter.py -s
````