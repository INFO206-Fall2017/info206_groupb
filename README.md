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
cd starter_slackbot
pipenv run python3 Scripts/starterbot.py

export BOT_ID=YOUR_BOT_ID
export SLACK_BOT_TOKEN=YOUR_SLACK_BOT_TOKEN
python starter_slackbot/Scripts/starterbot.py
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