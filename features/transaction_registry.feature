Feature: Transaction registry

  Scenario: User is able to create 2 transactions
    Given Transaction registry is empty
    When I create a transaction amount: "100", category: "Food"
    And I create a transaction amount: "2000", category: "Salary"
    Then Number of transactions in registry equals: "2"

  Scenario: User is able to update category of already created transaction
    Given Transaction registry is empty
    And I create a transaction amount: "50", category: "Bus"
    When I update "category" of transaction with category: "Bus" to "Transport"
    Then Transaction with category "Transport" exists in registry

  Scenario: User is able to delete created transaction
    Given Transaction registry is empty
    And I create a transaction amount: "300", category: "Shopping"
    When I delete transaction with category: "Shopping"
    Then Number of transactions in registry equals: "0"

  Scenario: User checks account summary and balance
    Given Transaction registry is empty
    When I create a transaction amount: "1000", category: "Salary"
    And I create a transaction amount: "200", category: "Food"
    Then The account balance should be "800.0"
    And The budget status should be "No limit set"
  
  Scenario: System prevents creating transaction with negative amount
    Given Transaction registry is empty
    Then I cannot create a transaction with amount: "-100", category: "Scam"