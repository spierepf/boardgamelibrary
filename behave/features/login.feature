@login
Feature: Login

  Background:
    Given the following users exist:
      | username         | password  |
      | test@example.com | password1 |


  Scenario: Make sure the not logged in steps work
    Given we are not logged in
    Then we will not be logged in


  Scenario: Make sure the logged in steps work
    Given we are logged in as "test@example.com"
    Then we will be logged in as "test@example.com"


  Scenario: Login dialog button appears when nobody is logged in
    Given we are not logged in
    When we direct the browser to "/"
    Then we will see a component with id "open_login_dialog"


  Scenario: User menu button appears when someone is logged in
    Given we are logged in as "test@example.com"
    When we direct the browser to "/"
    Then we will see a component with id "open_user_menu"


  Scenario: Clicking the login dialog button opens the login dialog
    Given we are not logged in
    When we direct the browser to "/"
    And we click on the component with id "open_login_dialog"
    Then we will see a component with id "login_dialog"
    And we will see a component with id "username"
    And we will see a component with id "password"
    And we will see a component with id "submit_login"
    And we will see a component with id "cancel_login"


  Scenario: Clicking the user menu button opens the user menu
    Given we are logged in as "test@example.com"
    When we direct the browser to "/"
    And we click on the component with id "open_user_menu"
    Then we will see a component with id "user_menu"
    Then we will see a component with id "logout"


  Scenario: Clicking the user logout button logs the user out
    Given we are logged in as "test@example.com"
    When we direct the browser to "/"
    And we click on the component with id "open_user_menu"
    And we click on the component with id "logout"
    Then we will not be logged in


  Scenario: We can log in
    Given we are not logged in
    When we direct the browser to "/"
    And we click on the component with id "open_login_dialog"
    And we enter the value "test@example.com" into the text field component with id "username"
    And we enter the value "password1" into the text field component with id "password"
    And we click on the component with id "submit_login"
    Then we will be logged in as "test@example.com"


  Scenario: We can cancel a log in attempt
    Given we are not logged in
    When we direct the browser to "/"
    And we click on the component with id "open_login_dialog"
    And we click on the component with id "cancel_login"
    Then we will not see a component with id "login_dialog"
