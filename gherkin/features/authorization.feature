@authorization
Feature: Authorization

  Background:
    Given the following users exist:
      | username              | password  | groups    |
      | test@example.com      | password1 |           |
      | admin@example.com     | password2 | ADMIN     |
      | committee@example.com | password3 | COMMITTEE |


  Scenario Outline: Unauthenticated users can only access certain endpoints
    When we perform a GET request on "<endpoint>"
    Then we get a <expectedResponse> response

    Examples:
      | endpoint                 | expectedResponse |
      | /testOnly/               | 200              |
      | /testOnly/committeeOnly/ | 403              |
      | /testOnly/adminOnly/     | 403              |


  Scenario Outline: Authenticated users can access restricted endpoints
    Given we have authenticated as "<username>" with password "<password>"
    When we perform a GET request on "<endpoint>"
    Then we get a <expectedResponse> response

    Examples:
      | username              | password  | endpoint                 | expectedResponse |
      | test@example.com      | password1 | /testOnly/adminOnly/     | 403              |
      | test@example.com      | password1 | /testOnly/committeeOnly/ | 403              |
      | admin@example.com     | password2 | /testOnly/adminOnly/     | 200              |
      | admin@example.com     | password2 | /testOnly/committeeOnly/ | 403              |
      | committee@example.com | password3 | /testOnly/adminOnly/     | 403              |
      | committee@example.com | password3 | /testOnly/committeeOnly/ | 200              |
