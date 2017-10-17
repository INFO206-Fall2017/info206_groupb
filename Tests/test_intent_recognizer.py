import sys
sys.path.append(sys.path[0] + '/Slackbot')  

import unittest
from Slackbot import *
from Slackbot.intent_recognizer import IntentRecognizer, BARTQueryIntent, BusQueryIntent, HelpIntent

class IntentRecognizerTest(unittest.TestCase):
    def test(self):

      self.assertTrue(True)

    def test_bart(self):
      recognizer = IntentRecognizer()
      intent = recognizer.recognize("bart downtown berkeley richmond")
      self.assertIsInstance(intent, BARTQueryIntent)

    def test_bart2(self):
      recognizer = IntentRecognizer()
      intent = recognizer.recognize("bart 24th fremont")
      self.assertIsInstance(intent, BARTQueryIntent)

    def test_bus(self):
      recognizer = IntentRecognizer()
      intent = recognizer.recognize("bus College Av & Ashby Av 51B University Av & 9th St")
      self.assertIsInstance(intent, BusQueryIntent)

    def test_bus2(self):
      recognizer = IntentRecognizer()
      intent = recognizer.recognize("bus University Av & 9th St 51B College Av & Ashby Av")
      self.assertIsInstance(intent, BusQueryIntent)

    def test_help(self):
      recognizer = IntentRecognizer()
      intent = recognizer.recognize("help")
      self.assertIsInstance(intent, HelpIntent)

    def test_help(self):
      recognizer = IntentRecognizer()
      intent = recognizer.recognize("what is this")
      self.assertIsInstance(intent, HelpIntent)

if __name__ == '__main__':
    unittest.main()