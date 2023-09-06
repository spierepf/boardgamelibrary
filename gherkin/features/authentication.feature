@authentication
Feature: Authentication

  Background:
    Given the following users exist:
      | username         | password  |
      | test@example.com | password1 |

  Scenario: Authentication with the correct password succeeds
    When we authenticate as "test@example.com" with password "password1"
    Then we will have an access token

  Scenario: Authentication with an incorrect password fails
    When we authenticate as "test@example.com" with password "password2"
    Then we will not have an access token
