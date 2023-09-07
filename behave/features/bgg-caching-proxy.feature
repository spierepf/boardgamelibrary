@bgg-caching-proxy
Feature: BoardGameGeek Caching Proxy

  Scenario: The client configuration endpoint return a response with a bgg_base_url entry
    When we perform a GET request on "/api/clientConfiguration/"
    Then we get a 200 response
    And the response body will have a "bgg_base_url" entry
