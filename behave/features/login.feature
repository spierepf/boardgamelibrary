@login
Feature: Login

  Background:
    Given the following users exist:
      | username         | password  |
      | test@example.com | password1 |


  Scenario: Login button appears when nobody is logged in
    When we direct the browser to "/"
    Then we will see a component with id "open_login_dialog"


  Scenario: User menu button appears when someone is logged in
    Given we are logged in as "test@example.com"
    When we direct the browser to "/"
    Then we will see a component with id "open_user_menu"
