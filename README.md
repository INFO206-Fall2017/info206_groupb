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