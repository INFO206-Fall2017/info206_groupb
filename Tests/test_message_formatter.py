import unittest
import Slackbot
from Slackbot import *
from Slackbot.intent_responder import BARTQueryResponse, BusQueryResponse

class MessageFormatterTest(unittest.TestCase):
    def test(self):
      formatter = message_formatter.MessageFormatter()
      print('\nTesting format without response')
      slack_response = formatter.format(None)
      print(slack_response, '\n')
      self.assertIsNotNone(slack_response)

    def test_bart(self):
      formatter = message_formatter.MessageFormatter()
      print('\nTesting format without BARTQueryResponse')
      bart_response = BARTQueryResponse()
      slack_response = formatter.format(bart_response)
      print(slack_response, '\n')
      self.assertIsNotNone(slack_response)

    def test_bus(self):
      formatter = message_formatter.MessageFormatter()
      print('\nTesting format without BusQueryResponse')
      bart_response = BusQueryResponse()
      slack_response = formatter.format(bart_response)
      print(slack_response, '\n')
      self.assertIsNotNone(slack_response)

if __name__ == '__main__':
    unittest.main()