@bgg-autocomplete
Feature: BoardGameGeek Autocomplete

  Scenario: Visiting the boardgamegeek autocomplete component test page
    When we direct the browser to "/test/bggAutocomplete"
    Then we will see a component with id "bgg-autocomplete"
    And we will see a component with id "selected-item-bgg-id"
    And we will see a component with id "selected-item-primary-name"
    And we will see a component with id "selected-item-year-published"


  Scenario: Before entering a title into a boardgamegeek autocomplete component
    When we direct the browser to "/test/bggAutocomplete"
    And we click on the component with id "bgg-autocomplete"
    Then the autocomplete component with id "bgg-autocomplete" will have an item "No data available"


  Scenario Outline: Entering a recognized title into a boardgamegeek autocomplete component
    When we direct the browser to "/test/bggAutocomplete"
    And we enter the value "<user-input>" into the component with id "bgg-autocomplete"
    Then the autocomplete component with id "bgg-autocomplete" will have an item "<display-name>"

    Examples:
      | user-input              | display-name                   |
      | Crossbows and Catapults | Crossbows and Catapults (1983) |
      | Senet e Tablan          | Senet e Tablan                 |


  Scenario Outline: Selecting a recognized title in a boardgamegeek autocomplete component combobox
    When we direct the browser to "/test/bggAutocomplete"
    And we enter the value "<user-input>" into the component with id "bgg-autocomplete"
    And we click on the "<display-name>" option in the autocomplete component with id "bgg-autocomplete"
    Then the text-field with id "selected-item-bgg-id" will contain "<bgg-id>"
    And the text-field with id "selected-item-primary-name" will contain "<primary-name>"
    And the text-field with id "selected-item-year-published" will contain "<year-published>"
    And the text-field with id "bgg-autocomplete" will contain "<display-name>"

    Examples:
      | user-input              | display-name                   | bgg-id | primary-name            | year-published |
      | Crossbows and Catapults | Crossbows and Catapults (1983) | 2129   | Crossbows and Catapults | 1983           |
      | Senet e Tablan          | Senet e Tablan                 | 328628 | Senet e Tablan          |                |


  Scenario: Entering an unrecognized title into a boardgamegeek autocomplete component
    When we direct the browser to "/test/bggAutocomplete"
    And we enter the value "There is no game with this title" into the component with id "bgg-autocomplete"
    Then the autocomplete component with id "bgg-autocomplete" will have an item "There is no game with this title"


  Scenario: Selecting an unrecognized title in a boardgamegeek autocomplete component combobox
    When we direct the browser to "/test/bggAutocomplete"
    And we enter the value "There is no game with this title" into the component with id "bgg-autocomplete"
    And we click on the "There is no game with this title" option in the autocomplete component with id "bgg-autocomplete"
    Then the text-field with id "selected-item-bgg-id" will contain "none"
    And the text-field with id "selected-item-primary-name" will contain "There is no game with this title"
    And the text-field with id "selected-item-year-published" will contain ""


  Scenario: An unstarted boardgamegeek autocomplete component is blank
    When we direct the browser to "/test/bggAutocomplete"
    Then the autocomplete component with id "bgg-autocomplete" will contain ""


  Scenario: An uncompleted boardgamegeek autocomplete component contains the entered text
    When we direct the browser to "/test/bggAutocomplete"
    And we enter the value "Crossbows and Catapults" into the component with id "bgg-autocomplete"
    Then the autocomplete component with id "bgg-autocomplete" will contain "Crossbows and Catapults"


  Scenario: A completed boardgamegeek autocomplete component contains the completed text
    When we direct the browser to "/test/bggAutocomplete"
    And we enter the value "Crossbows and Catapults" into the component with id "bgg-autocomplete"
    And we click on the "Crossbows and Catapults (1983)" option in the autocomplete component with id "bgg-autocomplete"
    Then the autocomplete component with id "bgg-autocomplete" will contain "Crossbows and Catapults (1983)"


  Scenario: When a completed boardgamegeek autocomplete component loses focus its text does not change
    When we direct the browser to "/test/bggAutocomplete"
    And we enter the value "Crossbows and Catapults" into the component with id "bgg-autocomplete"
    And we click on the "Crossbows and Catapults (1983)" option in the autocomplete component with id "bgg-autocomplete"
    And we click on the component with id "selected-item-primary-name"
    Then the autocomplete component with id "bgg-autocomplete" will contain "Crossbows and Catapults (1983)"
