@web-client
Feature: Web Client

  Scenario: The web client is available
    When we direct the browser to "/#/"
    Then we will see a component with id "app"