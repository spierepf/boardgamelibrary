@create-new-copy
Feature: Create library items

  Background:
    Given the following users exist:
      | username              | password  | groups    |
      | test@example.com      | password1 |           |
      | admin@example.com     | password2 | ADMIN     |
      | committee@example.com | password3 | COMMITTEE |


  Scenario Outline: Only certain users can see the "Create Library Items" button
    Given we are logged in as "<username>"
    When we click on the component with id "open_user_menu"
    Then we <will_or_will_not> see a component with id "open_create_new_copy_form"

    Examples:
      | username              | will_or_will_not |
      | admin@example.com     | will             |
      | committee@example.com | will             |
      | test@example.com      | will not         |


  Scenario: The user menu is visible on the create library item dialog
    Given we are logged in as "admin@example.com"
    When we open the create new copy form
    Then we will see a component with id "open_user_menu"


  Scenario: The create library item dialog
    Given we are logged in as "admin@example.com"
    When we open the create new copy form
    Then we will see a component with id "create_new_copy_form"
    And we will see a component with id "copy_owner"
    And we will see a component with id "copy_title"
    And we will see a component with id "submit"


  Scenario: The create library item dialog will list all users when an admin user is logged in
    Given we are logged in as "admin@example.com"
    When we open the create new copy form
    Then the select component with id "copy_owner" will have an item "admin@example.com"
    And the select component with id "copy_owner" will have an item "committee@example.com"
    And the select component with id "copy_owner" will have an item "test@example.com"


  Scenario: The create library item dialog will list only the logged in user when a committee user is logged in
    Given we are logged in as "committee@example.com"
    When we open the create new copy form
    Then the select component with id "copy_owner" will have an item "committee@example.com"
    Then the select component with id "copy_owner" will not have an item "admin@example.com"
    Then the select component with id "copy_owner" will not have an item "test@example.com"


  Scenario Outline: The create library item dialog will use the logged in user as the copy owner by default
    Given we are logged in as "<username>"
    When we open the create new copy form
    Then the select component with id "copy_owner" will have the "<username>" item selected

    Examples:
      | username              |
      | admin@example.com     |
      | committee@example.com |


  Scenario: The create library item dialog will display a message when a new copy is created by an admin user
    Given we are logged in as "admin@example.com"
    When we create a copy of the 1983 edition of "Crossbows and Catapults" for the logged in user
    Then we will see a component with id "success_message_snackbar"


  Scenario: The create library item dialog will display a message when a new copy is created by a committee user
    Given we are logged in as "committee@example.com"
    When we create a copy of the 1983 edition of "Crossbows and Catapults" for the logged in user
    Then we will see a component with id "success_message_snackbar"


  Scenario Outline: The create library item dialog will create a new copy of the selected bgg title
    Given we are logged in as "admin@example.com"
    When we create a copy of the <year> edition of "<title>" for the logged in user
    Then we will see a component with id "success_message_snackbar"
    And there will be a title with the name "<title>" and bgg id <bgg_id>
    And there will be a copy of the title with bgg id <bgg_id> belonging to "admin@example.com"

    Examples:
      | title                   | year | bgg_id |
      | Crossbows and Catapults | 1983 |   2129 |
      | Talisman                | 1983 |    714 |


  Scenario Outline: The create library item dialog will not create a new title when the selected bgg title exists
    Given we have authenticated as "admin@example.com" with password "password2"
    And we have created a title with name "<title>" and bgg_id <bgg_id>
    And we are logged in as "admin@example.com"
    When we create a copy of the <year> edition of "<title>" for the logged in user
    Then we will see a component with id "success_message_snackbar"
    And there will be a title with the name "<title>" and bgg id <bgg_id>
    And there will be a copy of the title with bgg id <bgg_id> belonging to "admin@example.com"

    Examples:
      | title                   | year | bgg_id |
      | Crossbows and Catapults | 1983 |   2129 |
      | Talisman                | 1983 |    714 |


  Scenario: The create library item dialog will create a new copy of the selected non-bgg title
    Given we are logged in as "admin@example.com"
    When we open the create new copy form
    And we enter the value "Some Title" into the component with id "copy_title"
    And we click on the "Some Title" option in the autocomplete component with id "copy_title"
    And we click on the component with id "submit"
    Then we will see a component with id "success_message_snackbar"
    And there will be a title with the name "Some Title" and no bgg id
    And there will be a copy of the title named "Some Title" belonging to "admin@example.com"


  Scenario: The create library item dialog will create a new copy
    Given we are logged in as "admin@example.com"
    When we create a copy of the 1983 edition of "Crossbows and Catapults" for the logged in user
    Then we will see a component with id "success_message_snackbar"
    And there will be a copy of the title named "Crossbows and Catapults" belonging to "admin@example.com"


  Scenario: The snackbar message will identify the title when a new copy is created
    Given we are logged in as "admin@example.com"
    When we create a copy of the 1983 edition of "Crossbows and Catapults" for the logged in user
    Then we will see a component with id "success_message_snackbar"
    And the component with id "success_message_snackbar" will include the substring "Crossbows and Catapults"


  Scenario: The snackbar message will identify the owner when a new copy is created
    Given we are logged in as "admin@example.com"
    When we create a copy of the 1983 edition of "Crossbows and Catapults" for the logged in user
    Then we will see a component with id "success_message_snackbar"
    And the component with id "success_message_snackbar" will include the substring "admin@example.com"


  Scenario Outline: The create library item dialog will create a new copy of a game whose title includes an ampersand
    Given we are logged in as "admin@example.com"
    When we create a copy of the <year> edition of "<title>" for the logged in user
    Then we will see a component with id "success_message_snackbar"
    And there will be a copy of the title named "<title>" belonging to "admin@example.com"

    Examples:
      | title              | year |
      | Tigris & Euphrates | 1997 |
      | Light & Dark       | 2017 |
      | Hare & Tortoise    | 1973 |


  Scenario: An admin user can create a copy for another user
    Given we are logged in as "admin@example.com"
    When we create a copy of the 1983 edition of "Crossbows and Catapults" for "committee@example.com"
    Then we will see a component with id "success_message_snackbar"
    And there will be a copy of the title named "Crossbows and Catapults" belonging to "committee@example.com"


  Scenario: Creating a new copy leaves the copy_title autocomplete empty
    Given we are logged in as "admin@example.com"
    When we create a copy of the 1983 edition of "Crossbows and Catapults" for the logged in user
    Then the autocomplete component with id "copy_title" will contain ""


  Scenario: Clicking the snackbar close button hides the snackbar
    Given we are logged in as "admin@example.com"
    When we create a copy of the 1983 edition of "Crossbows and Catapults" for the logged in user
    And we click on the component with id "success_message_snackbar_close_button"
    Then we will not see a component with id "success_message_snackbar"


  Scenario: Clicking the submit button a second time will not create a second copy
    Given we are logged in as "admin@example.com"
    When we create a copy of the 1983 edition of "Crossbows and Catapults" for the logged in user
    And we click on the component with id "success_message_snackbar_close_button"
    And we click on the component with id "submit"
    Then we will not see a component with id "success_message_snackbar"
