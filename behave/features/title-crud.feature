@title-crud
Feature: Creation, retrieval, update, and deletion of titles
  Background:
    Given the following users exist:
      | username              | password  | groups    |
      | test@example.com      | password1 |           |
      | admin@example.com     | password2 | ADMIN     |
      | committee@example.com | password3 | COMMITTEE |


  @create
  Scenario: We can create a title without a bgg_id
    Given we have authenticated as "admin@example.com" with password "password2"
    When we perform a POST request on "/library/titles/" with json body '{"name":"Some Title"}'
    Then we get a 201 response
    And the result of "$.name" will be "Some Title"


  @create
  Scenario: We can create a title with a bgg_id
    Given we have authenticated as "admin@example.com" with password "password2"
    When we perform a POST request on "/library/titles/" with json body '{"name":"Crossbows and Catapults", "bgg_id":2129}'
    Then we get a 201 response
    And the result of "$.name" will be "Crossbows and Catapults"
    And the result of "$.bgg_id" will be "2129"
