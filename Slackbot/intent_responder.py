import sys
sys.path.append(sys.path[0] + '/../')  

import intent_recognizer
from intent_recognizer import BARTQueryIntent, BusQueryIntent, HelpIntent
from BART.bart import BartApi
from NextBus.NextBus import NextBusAPI

class BARTQueryResponse:
  def __init__(self, intent = None):
    self.routes = []

class BusQueryResponse:
  def __init__(self, intent = None):
    self.departures = []

class NamesNotFoundResponse:
  def __init__(self, intent = None):
    self.names = []

class IntentResponder: 
  def __init__(self):
    self.bart_api = BartApi()
    self.next_bus_api = NextBusAPI()

  def respond_to_intent(self, intent):
    if type(intent) is BARTQueryIntent:
      return self.respond_to_bart_intent(intent)
    elif type(intent) is BusQueryIntent: 
      return self.respond_to_bus_intent(intent)
    else:
      return HelpIntent()

  def respond_to_bart_intent(self, intent):
    try: 
      if intent.destination is None: 
        etd_dict = self.bart_api.first_leg_train_etd(origin_station_name=intent.origin)
      else:
        etd_dict = self.bart_api.first_leg_train_etd(origin_station_name=intent.origin,
                                                destination_station_name=intent.destination)
      response = BARTQueryResponse()
      response.routes = [{ 
        "origin": intent.origin, 
        "destination": dest,
        "departures": departures
      } for dest, departures in etd_dict.items()]

      return response
    except ValueError as e: 
      if e is not None:
        response = NamesNotFoundResponse()
        response.names.append({ "name": e.args[0], "type": "route" })
        return response

  def respond_to_bus_intent(self, intent):
    try: 
      origin = intent.origin.replace("&amp;", "&")
      etd_dict, route_found, stop_found = self.next_bus_api.BartRoutesResponse(stopInput=origin, routeInput=intent.route)
      if (not route_found) or (not stop_found):
        response = NamesNotFoundResponse()
        if not stop_found:
          response.names.append({ "name": intent.origin, "type": "stop" })
        if not route_found:
          response.names.append({ "name": intent.route, "type": "route" })
          
      else:
        response = BusQueryResponse()
        response.routes = [{
          "origin": intent.origin, 
          "direction": direction,
          "departures": departures
        } for direction, departures in etd_dict.items()]
      return response
    except KeyError as e:
      if e is not None:
        response = NamesNotFoundResponse()
        response.names.append({ "name": e.args[0], "type": "route" })
        return response
