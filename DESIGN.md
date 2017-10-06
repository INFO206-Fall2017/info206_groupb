BB Bot Design Document 
======================

Problem Statement
-----------------


Usecases
--------


Assumptions and Constraints 
---------------------------



Our constraints as a team
-------------------------


Architecture
------------


Implementation Plan
-------------------


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



