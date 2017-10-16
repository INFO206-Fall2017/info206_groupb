import sys
sys.path.append(sys.path[0] + '/Slackbot')  

import unittest
import requests
import json
import Slackbot
from Slackbot import *
from Slackbot.intent_responder import BARTQueryResponse, BusQueryResponse

webhook_url = 'https://hooks.slack.com/services/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'
headers = { 'Content-type': 'application/json' }

class MessageFormatterTest(unittest.TestCase):
    def test(self):
      # creates a class called formatter from the message formatter script
      formatter = message_formatter.MessageFormatter()
      print('\nTesting format without response')
      # calls the format method within the message formatter class
      slack_response = formatter.format(None)
      # prints out the attachments 
      print(slack_response, '\n')
      # send the HTTP request to slack
      r = requests.post(webhook_url, data=json.dumps(slack_response), headers=headers)
      self.assertIsNotNone(slack_response)

    def test_bart(self):
      # creates a new instance of the message formatter class
      formatter = message_formatter.MessageFormatter()
      # prints this message in the terminal
      print('\nTesting format without BARTQueryResponse')
      # set the variable bus_response to the bartqueryresponse
      bart_response = BARTQueryResponse()
      # here we set new values for the routes values
      bart_response.routes = [
        {
          "origin": "Downtown Berkeley",
          "destination": "Fremont",
          "departures": [
            "Leaving",
            "15",
            "30"
          ]
        },
        {
          "origin": "Downtown Berkeley",
          "destination": "SFO / Millbrae",
          "departures": [
            "2",
            "18",
            "22"
          ]
        }
      ]

      slack_response = formatter.format(bart_response)
      r = requests.post(webhook_url, data=json.dumps(slack_response), headers=headers)
      self.assertIsNotNone(slack_response)

    def test_bus(self):
      formatter = message_formatter.MessageFormatter()
      print('\nTesting format without BusQueryResponse')
      bus_response = BusQueryResponse()
      # we will need to check for direction AND destination
      bus_response.routes = [
        {
          "origin": "Macarthur Blvd & Grand Av",
          "route_name": "B",
          "direction": "Oakland",
          "departures": [
            "Leaving",
            "2",
            "18"
          ]
        },
        {
          "origin": "Macarthur Blvd & Grand Av",
          "route_name": "B",
          "destination": "San Francisco",
          "departures": [
            "3",
            "11",
            "17"
          ]
        }
      ]
      slack_response = formatter.format(bus_response)
      r = requests.post(webhook_url, data=json.dumps(slack_response), headers=headers)
      self.assertIsNotNone(slack_response)

if __name__ == '__main__':
    unittest.main()