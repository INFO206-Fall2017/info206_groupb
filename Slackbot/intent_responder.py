import intent_recognizer
from intent_recognizer import BARTQueryIntent, BusQueryIntent, HelpIntent
from bart import BartApi

class BARTQueryResponse:
  def __init__(self, intent = None):
    self.routes = []

class BusQueryResponse:
  def __init__(self, init = None):
    self.departures = []

class IntentResponder: 
  def __init__(self):
    self.bart_api = BartApi()

  def respond_to_intent(self, intent):
    if type(intent) is BARTQueryIntent:
      return self.respond_to_bart_intent(intent)
    elif type(intent) is BusQueryIntent: 
      return self.respond_to_bus_intent(intent)
    else:
      return HelpIntent()

  def respond_to_bart_intent(self, intent):
    etd_dict = self.bart_api.first_leg_train_etd(origin_station_name=intent.origin,
                                            destination_station_name=intent.destination)
    response = BARTQueryResponse()
    route = {
      "origin": intent.origin,
      "destination": intent.destination,
      "departures": etd_dict
    }
    response.routes = [route]
    return response

  def respond_to_bus_intent(self, intent):
    response = BusQueryResponse()
    # TODO: access you intent params here, for example, intent.origin
    # TODO: add attributes yto your response, for example response.route, response.departures
    return response