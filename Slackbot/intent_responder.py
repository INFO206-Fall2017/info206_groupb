import sys
sys.path.append(sys.path[0] + '/../')  

import intent_recognizer
from intent_recognizer import BARTQueryIntent, BusQueryIntent, HelpIntent
from BART.bart import BartApi
from NextBus.NextBus import NextBusAPI

class BARTQueryResponse:
  """Represents a query response for BART schedules"""
  def __init__(self, intent = None):
    self.routes = []

class BusQueryResponse:
  """Represents a query response for bus Schedules"""
  def __init__(self, intent = None):
    self.departures = []

class NamesNotFoundResponse:
  """Represents a response in the case that at least one of the station/route names is unknown"""
  def __init__(self, intent = None):
    self.names = []

class NoDeparturesResponse:
  """Represents a response in the case that there's no schedule for departure for that specific route/station"""
  def __init__(self, intent = None):
    pass

class IntentResponder: 
  """Implments a responder that respond to intents"""
  def __init__(self):
    self.bart_api = BartApi()
    self.next_bus_api = NextBusAPI()

  def respond_to_intent(self, intent):
    """Respond to an intent. Returns different type of Response object according to the intent received."""
    if type(intent) is BARTQueryIntent:
      return self.respond_to_bart_intent(intent)
    elif type(intent) is BusQueryIntent: 
      return self.respond_to_bus_intent(intent)
    else:
      return HelpIntent()

  def respond_to_bart_intent(self, intent):
    """
    Specifically handle BARTQueryIntent by calling BART's API Wrapper.
    Returns a NoDeparturesResponse if there's currently no departures,
      NamesNotFoundResponse if at least one of the station/route names is unknown,
      or BARTQueryResponse if the API wrapper returned valid departure times.
    """
    try: 
      if intent.destination is None: 
        etd_dict = self.bart_api.first_leg_train_etd(origin_station_name=intent.origin)
      else:
        etd_dict = self.bart_api.first_leg_train_etd(origin_station_name=intent.origin,
                                                destination_station_name=intent.destination)

      if not etd_dict:
        response = NoDeparturesResponse()
        return response
      else: 
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
    """
    Specifically handle BusueryIntent by calling NextBus's API Wrapper.
    Returns a NoDeparturesResponse if there's currently no departures,
      NamesNotFoundResponse if at least one of the stop/route names is unknown,
      or BusQueryResponse if the API wrapper returned valid departure times.
    """
    try: 
      origin = intent.origin.replace("&amp;", "&")
      etd_dict, route_found, stop_found = self.next_bus_api.BartRoutesResponse(stopInput=origin, routeInput=intent.route)
      if (not route_found) or (not stop_found):
        response = NamesNotFoundResponse()
        if not stop_found:
          response.names.append({ "name": intent.origin, "type": "stop" })
        if not route_found:
          response.names.append({ "name": intent.route, "type": "route" })
      elif not etd_dict:
        response = NoDeparturesResponse()
        return response

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
