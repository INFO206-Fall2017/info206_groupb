BB Bot Design Document 
======================

Problem Statement
-----------------

Our program will create a slack bot that fetches and displays upcoming BART train and bus departure times based on user input. 

Usecases
--------

Our users will be those that use the School of Information Slack and rely on public transportation. The full process will behave as follows:
1. Users send the bot a direct message or invite it into a Slack channel.
2. Users can request information about a particular bus or BART stop.
3. The bot will format the user’s request and send it to either the NextBus or BART API, as appropriate.
4. The bot will format the response it receives and display upcoming departure times for that stop.


Assumptions and Constraints 
---------------------------
Our users can interact with our slackbot by sending direct messages. We expect the input to be in a special format(described below). Our BB Bot would prompt the user to input their response in this special format. BB Bot would provide user with directions and sample responses to help them frame their search request in the desired format. The user can chose to enter their input in one of the following format. The BB Bot would also provide the user with a link to access the names all BART and NextBus stations.

### CASE A: For BART search request

#### Option 1
User can input name of station( “Departing from” station ) and BART line. In this case, the user has information about the specific BART line that he/she want to board.
Input format:  BART    Station name       BART line
This input search will display the time schedule of next BART available from the input BART station for the input BART line (only). For example the input BART Downtown Berkeley Richmond would only display the time schedule of the next BART train from Downtown Berkeley station towards Richmond Line.

#### Option 2
Users can only input the name of station ( “Departing from” station) without specifying a BART  line
Input format:  BART    Station name 
This input search will display a list of time schedules for all BART line from the input BART station. For example the input BART Richmond will provide the user the time schedules for the next available BART for all lines such as Richmond, Daly City, Warm Springs/South Fremont, Fremont, Pleasanton/Dublin, Pittsburg/Bay Point.

### CASE B: For NextBus search request

#### Option 1
User can input name of NextBus stop (“Departing from” bus stop), route, and direction to receive departure information of buses for a specific bus route. 
Input format:  NextBus     Stop     Route     Direction
E.g. “NextBus 40th St & Telegraph Av 57 Emeryville”  

#### Option 2 Users can only input the name of NextBus stop (“Departing from” bus stop) without specifying any other parameters.
Input format:  NextBus    Stop
E.g. “NextBus 40th St & Telegraph Av
This input search will display a list of all bus routes in all directions from the input bus stop. 

The first input NextBus/BART will used to decide which function/classes will be called in our python program.  Our program will then convert the user “from” bus stops/Bart stations input to a format that can be used to send a request query to NextBus/BART api in order to get information from their database. For instance if our user wants to catch the nearest BART from Downtown Berkeley towards Fremont line. The user will enter name of station and line name as their input. The slackbot will recognize accept station names and line names as valid input. The slackbot will in turn send a request to BART api by converting it to a format that the BART api can understand (DBRK and FRMT in this case). 

In case, the user enters an incorrect input - say name of non-existent bus stop/BART station; the user will be prompted to modify their responses to display the correct name bus stop/BART value. Our program will execute to find the next available bus/BART that runs in the specific route+direction/ BART line and generate an output. The output will display the time after which the user can board the next bus/bart in option 1 of Case A and B. The output will display the name of all bus routes+directions / BART lines followed by the time after which the next available bus/BART are available for these routes/BART lines from the input bus stop/BART station. 

The output generated from our python program will then be formatted and send back to slack. This will be displayed to user via slack bot as a message. 


Our constraints as a team
-------------------------
We understand that the user will have to input the the exact name of the bus stop/BART station to request information using our slack bot.  For example if a user wants to board a BART form 12th St. Oakland City Center to Fremont. In order to request train information using our slack bot, the user will have to input the “Departing from?” station as “12th St. Oakland City Center”. Input such as 12th Street Oakland City Center, 12th St Oakland City Center, 12th St Oakland City Center, 12 St Oakland City Center, 12th St Okland City Center or Oakland City Center would be invalid. Though we would like to take care of such cases and accommodate for minor spelling mistakes by suggesting the correct station name. Due to time constraints, we would not be able to provide suggestions to our users in cases described above. The user will instead be provided a link to access the list of all BART stations and NextBus stops - to help them input the correct name of stations/bus stops. 

Similarly, though we would like to have a “Plan Ahead” feature in our slack bot that can help our user plan for a future trip by specifying a “departing around” and “arriving around” time - the BART api offers extracting information for future schedule by specifying - expected time of travel, date of travel, origin and destination station. A similar prediction request is supported by NextBus api structure. Our team, however, will not be able to implement this feature in our BB Bot due to time constraint.

However, If time permits, we will provide the user the option of entering two BART stations - the departing from(A) and the arriving at station(B). The user would not need to enter the BART line in this case. The output will return the time for next BART that would help user to reach point B  from point A.


Architecture
------------
The major features of the bot includes
* Responding to the user’ query about the schedules from a specific  BART station
* Responding to the user’s query about the schedules from a specific Bus station

At the top level, the bot will run as a Python program that interacts with Slack’s Real-time messaging (RTM) API. The program will also include a simple HTTP server to keep itself running on Heroku. 

![architecture](https://github.com/INFO206-Fall2017/info206_groupb/raw/master/Doc/top-level-architecture.jpg)


The architecture for the BB Bot itself can be illustrated as follows:

![architecture](https://github.com/INFO206-Fall2017/info206_groupb/raw/master/Doc/bot-architecture.jpg)

The major components includes :
### Message Handler
The component listens to the messages received via Slack RTM API and filters out messages irrelevant to the operation of the bot (i.e. messages that do not mention the bot). It then passes the relevant messages to the Intent Recognizer

### Intent Recognizer
The module recognizes the real intent and entities from a message. For example, the module should be able to recognize “bart richmond fremont” to a RouteQueryIntent with “Richmond” and “Fremont” as the entities.

### Intent Responder
Respond to the intent recognized by gathering data from the right APIs, format it, and send a response back to the user. 

### Data API Wrappers
Simplify the process of interacting with BART and NextBus APIs. The modules should provide python methods for the intent responder to call.
  
### Message Formatter
Formats the messages to be sent back to the user. 

The components will work together to handle user’s messages as shown in this pseudo code. 

```
On message received from Slack do:
  For message in all messages:
    If message relevant to the bot:
      (Intent and Entities) = RecognizeIntent(message)
      If Intent is IntentType1:
        Response = RespondToIntentType1(Intent, Entities)
        FormattedResponse = FormatMessage(Response)
        SendMessageBackToSlack(FormattedResponse)
      If Intent is IntentType2:
        Response = RespondToIntentType2(Intent, Entities)
        FormattedResponse = FormatMessage(Response)
```

Implementation Plan
-------------------

### Intent Recognition
We will use [Wit.ai](https://wit.ai/) for intent recognition. We’ll first build a conversational model in Wit.ai with the following intents
* BART Query Intent: 
  Indicates that the user would like to ask for BART schedules.
* Bus Query Intent: 
  Indicates that the user would like to ask for bus schedules.
* Help Intent:
  Indicates that the user needs help on how to use the bot.
  We’ll then use the conversational model from python via Wit.ai’s REST API.


### API Wrapper
The API wrappers will be developed by our team members using python’s `request` library to consume NextBus API (with XML) and BART API (with json).

### Message Formatting
The message formatter will be developed by our team members. We’ll use the Slack API to format messages as described in Slack’s [message formating document](https://api.slack.com/docs/message-formatting  )  

### Object Oriented Design

Our data classes includes

#### Intent Classes

* Intent
  Represents the base class for intents
* BARTQueryIntent (a subclass of Intent)
  Represents an user’s intent to query for BART schedules Attributes:
  * origin (string): The origin BART station
  * destination: (string, optional): The destination BART station.
  The class expects the destination to be non-null.
* BusQueryIntent (a subclass of Intent)
  Represents a user’s intent to query for bus schedules
  Attributes:
  * origin (string): The origin bus station
  * route (string): The AC Transit bus route in question, for example “6”, “51B”
  * direction (string, optional): The direction in question, for example, “Northbound” 
  * destination (string, optional): The destination bus station
  The class expects either of the direction or the destination to be non-null.
* HelpIntent (a subclass of Intent)
  Represents a user’s intent to ask for help on using the bot.

#### Response Classes
* BARTRoutesResponse
  Represents a response containing BART route schedules
  Attributes:
  * routes (list of BARTRoute): The routes and its schedule of departures 
* BusRoutesResponse
  Represents a response containing bus route schedules
  Attributes:
  * departures (list of  DateTime): The schedule of departures from that specific route.

### Feature breakdown:

* Slackbot setup (python): 
  * Member: All team members
  * Estimated effort: 1 mandays

* Slackbot setup (Heroku): 
  * Member: Soravis
  * Estimated effort: 0.5 mandays

* BART api access: 
  * Member: Anu
  * Estimated Completion Date: 10/10

* Nextbus api access:
  * Member: Dylan
  * Estimated Completion Date: 10/10

* Slackbot Intent Recognizer on Wit.ai:
  * Member: Soravis
  * Estimated effort: 3 mandays

* Message formatter:
  * Member: Devin 
  * Estimated effort: 3 mandays

* Integration & Testing
  * Members: all
  * Estimated completion: 10/16


Test Plan
---------

We planned to use three types of tests in our project: unit testing, integration testing and user acceptance testing.

### Unit Testing

We will have automated unit tests on our major modules include:

* Intent Recognizer Test Cases: 
  * Tests if the intent recognizer returns an Intent given different input strings. The test cases will not check the correctness of the intent as it largely depend on the model built on Wit.ai.

* Intent Responder Test Cases: 
  * Tests if the intent responder returns a correct Response object given different intents.

* Message Formatter Test Cases: 
  * Tests if the message formatter returns a Slack compatible json object given different Response object.



### Integration Testing

We will conduct an automated end-to-end test of the slackbot by injecting different input strings into the handle_message() function and expect it to return the correct Slack-compatible json object representing the response. Each integration test cases will include different input strings the users might send 
to the bot. 


### User Acceptance Testing (UAT)

We will use specific test cases to test each one of the BB Bot’s proposed functionalities. 

* Test Case 1:  User inputs the format incorrectly and slackbot responds with the correct format so the user is informed how to input route information in correctly.
  * Functionality: Help message for correct format.

* Test Case 2: User types in “@BBbot Bart Downtown Berkeley Station Richmond” and should be able to see all Richmond bound train departure information for the near future at the Downtown Berkeley Station.
  * Functionality: User accesses bus and train departure information from BART API by sending direct message to bot.

* Test Case 3: User types in “@BBbot Nextbus Macarthur Blvd & Grand Av Oakland” and should be able to see all Oakland bound bus departure information for the near future at the Macarthur Blvd & Grand Ave station.
  * Functionality: User accesses bus and train departure information from Nextbus API by sending direct message to bot.

* Test Case 4: User is provided map, station name information, and name lists for Bart and NextBus when using BBbot and before entering in route information.
  * Functionality: Default bot functionality includes providing the user with a URL that provides map and station name information.



