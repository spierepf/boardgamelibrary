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
    When we perform a POST request on "/api/library/titles/" with json body '{"name":"Some Title"}'
    Then we get a 201 response
    And the result of "$.name" will be "Some Title"


  @create
  Scenario: We can create a title with a bgg_id
    Given we have authenticated as "admin@example.com" with password "password2"
    When we perform a POST request on "/api/library/titles/" with json body '{"name":"Crossbows and Catapults", "bgg_id":2129}'
    Then we get a 201 response
    And the result of "$.name" will be "Crossbows and Catapults"
    And the result of "$.bgg_id" will be "2129"


  @create
  Scenario: Unauthenticated users cannot create titles
    Given we have not authenticated
    When we perform a POST request on "/api/library/titles/" with json body '{"name":"Some Title"}'
    Then we get a 401 response


  @create
  Scenario Outline: Only admin and committee users can create titles
    Given we have authenticated as "<username>" with password "<password>"
    When we perform a POST request on "/api/library/titles/" with json body '{"name":"Some Title"}'
    Then we get a <expectedResponse> response

    Examples:
      | username              | password  | expectedResponse |
      | test@example.com      | password1 | 403              |
      | admin@example.com     | password2 | 201              |
      | committee@example.com | password3 | 201              |


  @create
  Scenario: We cannot create multiple titles with the same bgg_id
    Given we have authenticated as "admin@example.com" with password "password2"
    And we have created a title with name "Crossbows and Catapults" and bgg_id 2129
    When we perform a POST request on "/api/library/titles/" with json body '{"name":"Crossbows and Catapults", "bgg_id":2129}'
    Then we get a 500 response


  @retrieve
  Scenario: We can retrieve a list of titles
    Given we have authenticated as "admin@example.com" with password "password2"
    And we have created a title with name "Crossbows and Catapults" and bgg_id 2129
    And we have created a title with name "Some Title"
    When we perform a GET request on "/api/library/titles/"
    Then we get a 200 response
    And the result of "$[0].name" will be "Crossbows and Catapults"
    And the result of "$[0].bgg_id" will be "2129"
    And the result of "$[1].name" will be "Some Title"
    And the result of "$[1].bgg_id" will be "None"
