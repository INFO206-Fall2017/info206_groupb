import sys
sys.path.append(sys.path[0] + '/Slackbot')  

import unittest
from Slackbot import *
from Slackbot.intent_recognizer import BARTQueryIntent, BusQueryIntent
from Slackbot.intent_responder import IntentResponder, BARTQueryResponse, BusQueryResponse

class IntentResponderTest(unittest.TestCase):
    def test(self):
      self.assertTrue(True)

    def test_bart(self):
      print('\nTesting BART Intent Responder')
      responder = IntentResponder()
      intent = BARTQueryIntent()
      intent.origin = "DBRK"
      intent.destination = "RICH"
      response = responder.respond_to_intent(intent)
      print(response)
      self.assertIsInstance(response, BARTQueryResponse)

    def test_bus(self):
      print('\nTesting Bus Intent Responder')
      responder = IntentResponder()
      intent = BusQueryIntent()
      intent.origin = "macarthur and maple"
      intent.route = "57"
      intent.destination = "emeryville"
      response = responder.respond_to_intent(intent)
      print(response)
      self.assertIsInstance(response, BusQueryResponse)

if __name__ == '__main__':
    unittest.main()