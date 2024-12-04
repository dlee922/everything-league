# everything-league
Things to retrieve from json match file:
-  riotIdGameName
  - info -> participants -> riotIdGameName


What I have built so far:
- frontend can talk to the backend at the moment
  - not much user input at the moment
  - need to be able to enter the summoner name and tagline
  - create the match data file based off of that in the backend
  - which then populates all the front end data that the user will see
  - still going to go with the idea of populating a spreadsheet-esque component
- have a few methods that get some data
  - need to figure out what other data I want to get
- have to organize the frontend into more components
- need to start building a database to store the json data and have the state automatically update based on the information inside of the last match json file

Data flow:
A user logs in with username and password
  - log in page
  - authentication using mongoDB and bcrypt

Once a user logs in they will be displayed the main page
Main component will be the table with all of the players they have played with including themselves
Probably will just use a button to update the last played game
Should just update all the stats

Database:
_id
username
password
date_of_creation
data:
  - list of players
    - each player will have their associated data