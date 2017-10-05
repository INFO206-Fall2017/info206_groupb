from Slackbot import intent_recognizer
from Slackbot.intent_recognizer import BARTQueryIntent, BusQueryIntent, HelpIntent

class BARTQueryResponse:
  def __init__(self):
    self.routes = []

class BusQueryResponse:
  def __init__(self):
    self.departures = []

class IntentResponder: 
  def respond_to_intent(self, intent):
    if type(intent) is BARTQueryIntent:
      return self.respond_to_bart_intent(intent)
    elif type(intent) is BusQueryIntent: 
      return self.respond_to_bus_intent(intent)
    else:
      return HelpIntent()

  def respond_to_bart_intent(self, intent):
    response = BARTQueryResponse()
    # TODO: access you intent params here, for example, intent.origin
    # TODO: add attributes yto your response, for example response.routes
    return response

  def respond_to_bus_intent(self, intent):
    response = BusQueryResponse()
    # TODO: access you intent params here, for example, intent.origin
    # TODO: add attributes yto your response, for example response.route, response.departures
    return response