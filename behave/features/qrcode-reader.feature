@qrcode-reader
Feature: QRCode Reader

  Scenario: Visiting the qrcode reader component test page
    When we direct the browser to "/test/qrcodeReader"
    Then we will see a component with id "qrcode-reader"
    And we will see a component with id "decode-type"
    And we will see a component with id "decode-uuid"


  Scenario Outline:
    When we direct the browser to "/test/qrcodeReader"
    And we scan the qrcode "<qrcode>" into the qrcode reader component with id "qrcode-reader"
    Then the text-field with id "decode-type" will contain "<decode-type>"
    And the text-field with id "decode-uuid" will contain "<decode-uuid>"

    Examples:
      | qrcode                                     | decode-type | decode-uuid                          |
      | P.42902eba-c6c2-4975-a453-1a9cc7a14486.png | P           | 42902eba-c6c2-4975-a453-1a9cc7a14486 |
      | I.170172db-696d-4348-8b7d-e061c60ca751.png | I           | 170172db-696d-4348-8b7d-e061c60ca751 |
      | invalid-type.png                           |             |                                      |
      | invalid-uuid.png                           |             |                                      |
