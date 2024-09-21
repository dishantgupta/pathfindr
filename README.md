#  [PathFindr] Amadeus Flight Offers Integration Service 


## _Introduction_

This is a Python based Flask Application exposed on uWSGI web server. It is used to fetch cheapest flight information from third party services. As of now, only one client integration is active (Amadeus). To enable the said client integration, application would need the following env variables - 

- AMADEUS_API_KEY
- AMADEUS_API_SECRET_KEY

The application APIs can be accessed on: localhost:8080

## _APIs_

- /flights/ping

> curl --location 'localhost:8080/flights/ping'

- /flights/price

> curl --location 'localhost:8080/flights/price?origin=jfk&destination=LAX&date=2024-09-24&nocache=true'
> curl --location 'localhost:8080/flights/price?origin=jfk&destination=LAX&date=2024-09-24'

## _Workflow_

- startup
-- on application startup, Amadeus Access Token is generated and cached by the system for 30 mins

- healthCheck
-- health check API retruns static response to verify if application is responding

- fetch offers
-- Amadeus flight offers API responses are cached by the system based on {origin, destination, departure-date} combination for 10 mins
-- sending {nocache=True} to flight offers API, explicitly fetches fresh data from Amadeus API and caches the same
-- when Amadeus Access Token is expired, the token is refreshed and again cached by the system


## _Run_

To run the application run the following command from the application directory
> docker-compose run --env AMADEUS_API_KEY={} AMADEUS_API_SECRET_KEY={}
> docker-compose up --build


## _Further Enhancements_

- uWSGI server integration [CRITICAL]
  - flask server is not for production usecase, a web server needs to be integrated which redirects to flask server

- Test Cases - Mock Amadeus API [CRITICAL]
  - mock client APIs and write test scenarios for success and fail cases
  - connection errors, http errors, invalid inputs need to be mocked for Amadeus authentication and flight offers APIs
  - test cases validation should be done at app startup

- abstraction of flight client [HIGH]
  - integrate multiple clients
  - dynamically switch clients based on a property or configuration
