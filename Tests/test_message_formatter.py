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
      formatter = message_formatter.MessageFormatter()
      print('\nTesting format without response')
      slack_response = formatter.format(None)
      print(slack_response, '\n')
      r = requests.post(webhook_url, data=json.dumps(slack_response), headers=headers)
      self.assertIsNotNone(slack_response)

    def test_bart(self):
      formatter = message_formatter.MessageFormatter()
      print('\nTesting format without BARTQueryResponse')
      bart_response = BARTQueryResponse()
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
      print(slack_response, '\n')
      r = requests.post(webhook_url, data=json.dumps(slack_response), headers=headers)
      self.assertIsNotNone(slack_response)

    def test_bus(self):
      formatter = message_formatter.MessageFormatter()
      print('\nTesting format without BusQueryResponse')
      bus_response = BusQueryResponse()
      bus_response.route = {
        "origin": "Emeryville",
        "route_name": "57",
        "destination": "Macarthur and Maple",
        "departures": [
          "Leaving",
          "2",
          "18"
        ]
      }
      slack_response = formatter.format(bus_response)
      print(slack_response, '\n')
      r = requests.post(webhook_url, data=json.dumps(slack_response), headers=headers)
      self.assertIsNotNone(slack_response)

if __name__ == '__main__':
    unittest.main()