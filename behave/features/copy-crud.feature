@copy-crud
Feature: Creation, retrieval, update, and deletion of copies
  Background:
    Given the following users exist:
      | username              | password  | groups    |
      | test@example.com      | password1 |           |
      | admin@example.com     | password2 | ADMIN     |
      | committee@example.com | password3 | COMMITTEE |


  @create
  Scenario: Created copies refer to their titles
    Given we have authenticated as "admin@example.com" with password "password2"
    When we create a copy of "Some Title" belonging to "admin@example.com"
    And we perform a GET request on the result of "$.title"
    Then the result of "$.name" will be "Some Title"


  @create
  Scenario: Created copies refer to their owners
    Given we have authenticated as "admin@example.com" with password "password2"
    When we create a copy of "Some Title" belonging to "admin@example.com"
    And we perform a GET request on the result of "$.owner"
    Then the result of "$.username" will be "admin@example.com"
