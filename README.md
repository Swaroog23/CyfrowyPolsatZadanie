## Overview
This repo contains two apps: Consumer and Provider.
They communicate through RabbitMQ.
Consumer is app with sole purpose of getting and saving data to Sqlite databse.
Provider accepts GET and POST request, then sends them via RabbitMQ to Consumer, and either informs user that operation was successful or returns an error code

## Dependencies
The main dependencies in this project are:
 - Aio-pika - for connection to RabbitMQ
 - Aiohttp - for web client
 Other dependencies are contained in requierments.txt

## Structure
There are two apps inside this repository: Provider and Consumer.

Provider is an aiohttp client, for user interaction, with rabbitmq publisher to send messages over broker to rabbitmq worker. It contains client.py, provider.py as well as validator for request body and reply from worker. Main.py app starts the application, and urls.py contains all urls for the app.

GET endpoint accepts `key` in its url, which must be numeric, and returns data from db under this key, if the key exists.

POST endpoint accepts json object `{<key>: <value>}`, where key must be numeric and value cannot be null and informs user if saving data to db was successful or not.

Consumer is an app which interacts with database, as well as accepts and replys to rabbitmq messages. It contains subfolder "Database" with logic to create, save, and retrive data from db. Worker.py is an main file for the app, as it starts the application, establishes queues and channels and consumes messages from the Provider and replys to it with requested data or information if operations were successful. 

Apps talk to eachother via two queues: one for get, one for post, which are connected to default exchange.

## Database
The database is created on start of the worker, in the Consumer container. It's an sqlite3 database file with one table "key_value" which stores key as primary key integer and value as text, which cannot be null.

## Constants
Both Provider and Consumer contain consts.py to store: queue names and rabbitmq host name. Additionally, Consumer has in its consts.py database name.

## Quickstart
App are contenerized via docker. Docker-compose contains everything needed to start the app, and both apps have their own Dockerfile, so to run the app use `docker-compose up --build`. 
To comunicate with the app, use something like Postman or Insomnia.

The url's are:
 - GET: /get-value/<key> - returns value under give key from database. If key does not exists, returns HTTP 400. Key must be a number, otherwise app returns 404.
 - POST: /add-valie/ - saves data to database, if body of a request is in correct format (accepts json, key must be numeric string and value cannot be null). If data is saved, app will inform user that data is saved, else returns HTTP 400.
