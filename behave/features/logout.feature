@logout
Feature: Logout

  Background:
    Given the following users exist:
      | username              | password  | groups    |
      | admin@example.com     | password2 | ADMIN     |


  Scenario: Clicking the logout button logs the user out
    Given we are logged in as "admin@example.com"
    When we direct the browser to "/"
    And we click on the component with id "open_user_menu"
    And we click on the component with id "logout"
    Then we will not be logged in


  Scenario: Clicking the logout button returns the browser to the home screen
    Given we are logged in as "admin@example.com"
    When we direct the browser to "/"
    And we open the create new copy form
    And we click on the component with id "open_user_menu"
    And we click on the component with id "logout"
    Then we will not see a component with id "create_new_copy_form"
