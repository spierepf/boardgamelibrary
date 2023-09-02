@startup
Feature: The application is started by environment.py

  Scenario: The application is successfully started
    When we perform a GET request on "/"
    Then we get a 200 response
