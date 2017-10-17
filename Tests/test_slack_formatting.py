import sys
sys.path.append(sys.path[0] + '/Slackbot')  

import unittest
import requests
import json
import Slackbot
from Slackbot import *
from Slackbot.intent_responder import BARTQueryResponse, BusQueryResponse

class SlackFormatterTest(unittest.TestCase):
    def test(self):
      webhook_url = 'https://hooks.slack.com/services/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'
      headers = { 'Content-type': 'application/json' }
      # message = {
      #   "text": "Thisss is a line of text from Python.\nAnd this is another one."
      # }

      message = {
        "attachments": [
          {
            "fallback": "Required plain-text summary of the attachment.",
            "color": "#36a64f",
            "pretext": "Optional text that appears above the attachment block",
            "author_name": "Bobby Tables",
            "author_link": "http://flickr.com/bobby/",
            "author_icon": "http://flickr.com/icons/bobby.jpg",
            "title": "Slack API Documentation",
            "title_link": "https://api.slack.com/",
            "text": "Optional text that appears within the attachment",
            "fields": [
              {
                "title": "Priority",
                "value": "High",
                "short": False
              }
            ],
            "image_url": "http://my-website.com/path/to/image.jpg",
            "thumb_url": "http://example.com/path/to/thumb.png",
            "footer": "Slack API",
            "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png",
            "ts": 123456789
          },
          {
            "fallback": "Required plain-text summary of the attachment.",
            "color": "red",
            "pretext": "Optional text that appears above the attachment block",
            "author_name": "Bobby Tables",
            "author_link": "http://flickr.com/bobby/",
            "author_icon": "http://flickr.com/icons/bobby.jpg",
            "title": "Slack API Documentation",
            "title_link": "https://api.slack.com/",
            "text": "Optional text that appears within the attachment 2",
            "fields": [
              {
                "title": "Priority",
                "value": "High",
                "short": False
              }
            ],
            "image_url": "http://my-website.com/path/to/image.jpg",
            "thumb_url": "http://example.com/path/to/thumb.png",
            "footer": "Slack API",
            "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png",
            "ts": 123456789
          }
        ]
      }
      r = requests.post(webhook_url, data=json.dumps(message), headers=headers)

if __name__ == '__main__':
    unittest.main()