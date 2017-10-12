import urllib.request
import xml.etree.ElementTree as ET
import
#https://docs.python.org/3.0/library/urllib.request.html
#https://docs.python.org/3/library/xml.etree.elementtree.html#xml.etree.ElementTree.XMLPullParser

class NextBusAPI(object):
    """
    Inputs:
        Stop (mandatory), e.g. "MacArthur Blvd & 66th Av"
        Route (mandatory), e.g. "57"
        Direction (optional), e.g. "Emeryville"

    Outputs:
    List of soon to depart buses, with:
        Route title
        Direction
        Departure Time Estimate

    Methods should accept BARTQueryIntent and return a BARTRoutesResponse.

    BusQueryIntent (a subclass of Intent)
		Represents a user’s intent to query for bus schedules
		Attributes:
            origin (string): The origin bus station
            Route (string): The AC Transit bus route in question, for example “6”, “51B”
            direction (string, optional): The direction in question, for example, “Northbound”

    BusRoutesResponse
		Represents a response containing bus route schedules
		Attributes:
            departures (list of  DateTime): The schedule of departures from that specific route.

    Assume NextBus object will be called once and then used repeatedly.
    """

    def __init__(self):
        """
        Initiate with values for AC transit, including a full list of stops.
        """
        #from Agency List
        self.agencyTag = 'actransit'
        self.agencyTitle = 'AC Transit'
        self.regionTitle = 'California-Northern'

    def getAgencyList(self):
        """
        Obtain a list of available transit agencies.
        """
        #Agency information
        #Import agency list feed and parse it into an Element Tree.
        self.agencyListFeed = urllib.request.urlopen('http://webservices.nextbus.com/service/publicXMLFeed?command=agencyList')
        self.agencyList = ET.parse(self.agencyListFeed)

    def getRouteList(self, agency):
        """
        http://webservices.nextbus.com/service/publicXMLFeed?command=routeList&a=<agency_tag>
        Obtain a list of routes for a given agency.
        The agency is specified by the "a" parameter in the query string.
        The tag for the agency is obtained from the agencyList command.
        """
        routeListFeed = urllib.request.urlopen('http://webservices.nextbus.com/service/publicXMLFeed?command=routeList&a=%s' %agency)
        routeList = ET.parse(routeListFeed)

        print("getRouteList url request: ", 'http://webservices.nextbus.com/service/publicXMLFeed?command=routeList&a=%s' %agency)

        #Get dictionary of route tag: route title
        routeListRoot = routeList.getroot()
        routeDictionary = {}
        for child in routeListRoot:
            routeDictionary.update({child.get('title'):child.get('tag')})

        return routeDictionary

    def getRouteConfig(self, agency, route):
        """
        http://webservices.nextbus.com/service/publicXMLFeed?command=routeConfig&a=<agency_tag>&r=<route tag>
        Obtain a list of routes for a given agency. The route is optionally specified by the "r" parameter.
        The tag for the route is obtained using the routeList command.
        If the "r" parameter is not specified, all routes for the agency are returned, limited to 100 routes per request.
        Returns a dictionary of {stop tag: stop title} for the given route.
        """
        routeConfigFeed = urllib.request.urlopen('http://webservices.nextbus.com/service/publicXMLFeed?command=routeConfig&a=%s&r=%s' %(agency, route))
        routeConfig = ET.parse(routeConfigFeed)

        print("getRouteConfig url request:", 'http://webservices.nextbus.com/service/publicXMLFeed?command=routeConfig&a=%s&r=%s' %(agency, route))

        #Create a dictionary with stop tags:stop titles.
        stopsDictionaryByTag = {}
        routeConfigRoot = routeConfig.getroot()
        for route in routeConfigRoot:
            for stop in route:
                stopsDictionaryByTag.update({stop.get('tag'):stop.get('title')})

        #print('Stops Dictionary by Tag:', self.stopsDictionaryByTag)
        return stopsDictionaryByTag


    def getPredictionRequest(self, agency, route, stop):
        """
        http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=<agency_tag>&r=<route tag>&s=<stop tag>
        Obtain predictions associated with a particular stop. There are two ways to specify the stop: 1) using a stopId or 2) by specifying the route and stop tags.​
        Returns a list of bus departure times, with the first item being the route direction.
        """
        print('getPredictionRequest url: ', 'http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=%s&r=%s&s=%s' %(agency, route, stop))
        self.predictionRequestFeed = urllib.request.urlopen('http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=%s&r=%s&s=%s' %(agency, route, stop))
        self.predictionRequest = ET.parse(self.predictionRequestFeed)

        busDepartureTimes = {}
        self.predictionRequestRoot = self.predictionRequest.getroot()
        for predictions in self.predictionRequestRoot:
            for direction in predictions:
                timeList = []
                for prediction in direction:
                    #print(prediction.items())
                    timeList.append(prediction.get('minutes'))
                busDepartureTimes[direction.get('title')] = timeList

        return busDepartureTimes




    def BartRoutesResponse(self, routeInput, stopInput, directionInput = None):
        """Takes stop, route, and optionally direction as input.
        Returns a dictionary with destinations as keys and a list of upcoming departure times as values."""


        #From route title, find route tag
        routeDictionary = self.getRouteList(self.agencyTag)
        #route dictionary will be defined, with title:tag


        routeTag = routeDictionary[routeInput]
        print('Route Input:', routeInput, 'Route Tag:', routeTag)

        #From stop title, find stop tags
        stopsDictionaryByTag = self.getRouteConfig(self.agencyTag, routeTag)

        #Clean up user's input so it matches something in stop tags
        #Should fix so that '40 and telegraph' matches 'Telegraph Av & 40th St'
        

        #Check stopsDictionaryByTag for all instances of the stop title, and fetch the associated tags
        stopTags = []
        for tag in stopsDictionaryByTag:
            if stopsDictionaryByTag[tag] == stopInput:
                stopTags.append(tag)

        print('Stop Input:', stopInput, 'Stop Tags:', stopTags)

        #Make prediction request, assign to dictionary
        departureTimes = {}
        for tag in stopTags:
            departureTimes.update(self.getPredictionRequest(self.agencyTag, routeTag, tag))


        #If a direciton input was specified, use only that direciton's results.
        if directionInput:
            departureTimes = {directionInput:departureTimes[directionInput]}

        print(departureTimes)
        return departureTimes

        """
        #make string of 'Destination1: time1 min, time2 min, time3 min\nDestination2: time min, time2 min, time3 min'
        departureStatement = "Upcoming departures of the %s line from %s:" %(routeInput, stopInput)

        for destination in departureTimes:
            departureStatement +=("\n%s:" %destination)
            for time in departureTimes[destination]:
                departureStatement += (' %s min,' %str(time))
            #Remove final comma
            if departureStatement[-1] == ',':
                departureStatement = departureStatement[0:len(departureStatement) -1]

        print(departureTimes)
        print(departureStatement)
        return(departureStatement)
        """


if __name__ == '__main__':
    NextBus = NextBusAPI()

    """
    #Test: Print agency list
    #NextBus.getAgency()
    agencyListRoot = NextBus.agencyList.getroot()
    agencies = []
    for child in agencyListRoot:
       agencies.append(child.get('title'))
    print('\n'.join(agencies))
    """
    """
    #Test: print route feed
    NextBus.getRouteList(NextBus.agencyTag)
    print(NextBus.routeDictionary)
    # routeListRoot = NextBus.routeList.getroot()
    # for child in routeListRoot:
    #     print(child.get('title'))
    """
    """
    #Test: print route config
    NextBus.routeTag = '57'
    NextBus.getRouteConfig(NextBus.agencyTag, NextBus.routeTag)
    print(NextBus.stopsDictionary)
    """
    """
    #Test: print prediction request
    NextBus.routeTag = '57'
    NextBus.stopTag = '1002650'
    NextBus.getPredictionRequest(NextBus.agencyTag, NextBus.routeTag, NextBus.stopTag)
    predictionRequestRoot = NextBus.predictionRequest.getroot()
    for child in predictionRequestRoot:
        print('Prediction request:', child.items())
        for item in child:
            print(item.items())
    """

    #Test: BARTRoutesResponse
    # NextBus.BartRoutesResponse(stopInput = "40th St & Telegraph Av", routeInput = "57", directionInput = "Foothill Square" )
    NextBus.BartRoutesResponse(stopInput = "40th St & Telegraph Av", routeInput = "57")
    # pass
