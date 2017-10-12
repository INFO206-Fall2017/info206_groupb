import requests
import json
from xml.etree import ElementTree as ET

def fetch_actransit_bus_routes_and_stops():
  # get actransit route list
  routes_url = 'http://webservices.nextbus.com/service/publicXMLFeed?command=routeList&a=actransit'
  r = requests.get(routes_url)
  tree = ET.fromstring(r.text)
  routes = []
  stops = []
  stops_dict = {}
  for child in list(tree.iter("route")):
    route = {
      "title": child.get('title'),
      "tag": child.get('tag'),
      "short_title": child.get('shortTitle')
    }
    routes.append(route)
    print("fetching stop info for " + str(route["tag"]))
    route_config_url = 'http://webservices.nextbus.com/service/publicXMLFeed?command=routeConfig&a=actransit&r=' + route["tag"] 
    r = requests.get(route_config_url)
    route_config_xml = ET.fromstring(r.text)
    route_xml = route_config_xml.find("route")
    for stop_xml in list(route_xml.iter("stop")):
      stop = {
        "tag": stop_xml.get("tag"),
        "title": stop_xml.get("title"),
        "stop_id": stop_xml.get("stopId")
      }
      # print(route["title"], route["tag"], stop["tag"], stop["title"], stop["stop_id"], sep="\t")
      if stop_xml.get("title") not in stops_dict:
        stops.append(stop)
        stops_dict[stop_xml.get("title")] = stop_xml.get("title")

  print('Number of routes ', len(routes))
  print('Number of stops ', len(stops))

  return (routes, stops)

def fetch_bart_stations():
  url = 'http://api.bart.gov/api/stn.aspx?cmd=stns&key=MW9S-E7SL-26DU-VV8V&json=y'
  r = requests.get(url)
  stations = r.json()["root"]["stations"]["station"]
  return stations

def fetch_bus_stations():
  pass

def to_snakecase(input_str):
  output_str = input_str.lower()
  output_str = output_str.replace(' ', '_')
  output_str = output_str.replace('.', '')
  output_str = output_str.replace('/', '_')
  output_str = output_str.replace('&', 'and')
  return output_str

def delete_legacy_bart_stop_entities():
  headers= { 'Authorization': 'Bearer ZORCO375BQH6IX2ZUQGJACGNAVDWWYGR', 'Content-Type': 'application/json' }
  stop_values = []
  stations = fetch_bart_stations()
  for stn in stations:
    val = to_snakecase(stn["name"])
    print("deleting " + val)
    r = requests.delete('https://api.wit.ai/entities/stop/values/' + val + '?v=20171010', headers=headers)

def update_bart_stop_entity():
  headers= { 'Authorization': 'Bearer ZORCO375BQH6IX2ZUQGJACGNAVDWWYGR', 'Content-Type': 'application/json' }
  stop_values = []
  stations = fetch_bart_stations()
  for stn in stations:
    stop_values.append({
      "value": stn["name"],
      "expressions": [stn["name"], stn["abbr"], 'zip ' + stn["zipcode"]],
      "metadata": to_snakecase(stn["name"])
    })

  print(stop_values)
  for stn in stop_values:
    r = requests.post('https://api.wit.ai/entities/stop/values?v=20171010', data=json.dumps(stn), headers=headers)
    print(r.json())

def update_bus_stop_entity():
  headers= { 'Authorization': 'Bearer ZORCO375BQH6IX2ZUQGJACGNAVDWWYGR', 'Content-Type': 'application/json' }
  stop_values = []
  route_values = []
  (routes, stops) = fetch_actransit_bus_routes_and_stops()
  for route in routes:
    route_values.append({
      "value": route["tag"],
      "expressions": [route["tag"], route["title"]],
      "metadata": route["tag"]
    })

  for route in route_values:
    r = requests.post('https://api.wit.ai/entities/bus_route/values?v=20171010', data=json.dumps(route), headers=headers)
    print(r.json())

  for stp in stops:
    if stp["title"] is not None:
      stop_values.append({
        "value": stp["title"],
        "expressions": [stp["title"]],
        "metadata": to_snakecase(stp["title"])
      })

  for stn in stop_values:
    r = requests.post('https://api.wit.ai/entities/stop/values?v=20171010', data=json.dumps(stn), headers=headers)
    print(r.json())
  

def main():
  update_bart_stop_entity()
  update_bus_stop_entity()
    

if __name__ == "__main__":
  main()