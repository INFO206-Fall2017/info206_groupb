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
      slack_response = formatter.format(None, None)
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

      # we will run this multiple times depending on the amount of routes given
      # we will also add a new argument in the function so the function repeats as many times as needed
      # we set slack_response to the output of the format function
      #######
      trainindex = 0
      while trainindex < len(bart_response.routes):
        slack_response = formatter.format(bart_response, trainindex)
        # prints the the attachments within slack_response
        print(slack_response, '\n')
        # tells slack to print out these values
        r = requests.post(webhook_url, data=json.dumps(slack_response), headers=headers)
        #######
        self.assertIsNotNone(slack_response)
        trainindex += 1

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
      busindex = 0
      while busindex < len(bus_response.routes):
        slack_response = formatter.format(bus_response, busindex)
        print(slack_response, '\n')
        r = requests.post(webhook_url, data=json.dumps(slack_response), headers=headers)
        self.assertIsNotNone(slack_response)
        busindex += 1

if __name__ == '__main__':
    unittest.main()