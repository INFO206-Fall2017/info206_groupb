# info206_groupb
Project:
For our project, we plan to create a slack bot that users can use to obtain real time data regarding bus and BART arrival and departure times. If time permits, we will add more features to the bot.

Team Members:
Devin Huang
Anu Pandey
Dylan Fox
Sun Soravis

## Requirements

* Python >= 3.6

## Getting Started

To get started, use the following command from the project root directory

``` sh
pip install pipenv # Install Pipenv if you do not have one
pipenv run python3 Slackbot/slackbot.py

export BOT_ID=YOUR_BOT_ID
export SLACK_BOT_TOKEN=YOUR_SLACK_BOT_TOKEN
python Slackbot/slackbot.py
```
## Production Deployment

This project supports hosting on heroku through Procfile and Pipfile. To run on heroku, copy the directory `starter_slackbot` outside of this repo to start a new local repository 

``` sh
cd starter_slackbot
git init
git add .
git commit -m "Initial Commit"
heroku create
heroku buildpacks:set heroku/python
heroku config:set BOT_ID=YOUR_BOT_ID
heroku config:set SLACK_BOT_TOKEN=YOUR_SLACK_BOT_TOKEN
git push heroku master
```

## NextBus

### NextBus XML Feed

[NextBus](https://www.nextbus.com/) offers an XML feed through which applications can request bus information. The full documentation is [here](https://www.nextbus.com/xmlFeedDocs/NextBusXMLFeed.pdf) , but we used the commands below. We also used **urllib.request** to get the URLs, and **xml.etree.ElementTree** to parse the returned XML.

The inputs from the user are a route (mandatory), stop (mandatory), and destination (optional). E.g. 'Telegraph and 40th 6 Foothill Square'.

#### Agency List

**Input: None**

**Output: List of agency tags**

Obtains a list of available transit agencies. Currently we've hardcoded it to use actransit, but with minimum modifications it could be used for any of NextBus's affiliate transit systems.

#### Route List

**Input: Agency tag**

**Output: List of routes for that agency**

We used this command to create a dictionary of routes that we could compare the user's route request against.

#### Route Config

**Input: Agency, Route**

**Output: List of stops for a given route**

We used this to create a dictionary of stops that we could compare the user's stop request against. Because NextBus requires a route for this command if more than 100 routes would be returned otherwise (and AC Transit has >150 routes), we require the user to enter a route, not just a stop.

#### Prediction Request

**Input: Agency, Route, Stop**

**Output: List of departure times for buses heading out from this stop; one list for each route destination.**

Finally, we use this command to generate the key information our users are after: upcoming departure times. If the user provided a destination, we filter the results to show only that destination. 

Our NextBus.py code returns a dictionary with keys of destination names and values of a list of upcoming departure times for that destination, as well as booleans indicating whether any routes or stops were returned that we use in handling errors.

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