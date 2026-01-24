from behave import step, when, then
import requests

URL = "http://localhost:5000"

@step('Transaction registry is empty')
def clear_transaction_registry(context):
    response = requests.get(URL + "/api/transactions")
    assert response.status_code == 200
    transactions = response.json()
    
    for t in transactions:
        t_id = t["transaction_id"]
        requests.delete(URL + f"/api/transactions/{t_id}")

@step('I create a transaction amount: "{amount}", category: "{category}"')
def create_transaction(context, amount, category):
    json_body = {
        "amount": float(amount),
        "category": category,
        "date": "2026-01-24"
    }
    create_resp = requests.post(URL + "/api/transactions", json=json_body)
    assert create_resp.status_code == 201

@step('Number of transactions in registry equals: "{count}"')
def is_transaction_count_equal_to(context, count):
    response = requests.get(URL + "/api/transactions")
    assert len(response.json()) == int(count)

@when('I update "{field}" of transaction with category: "{old_category}" to "{value}"')
def update_transaction_field(context, field, old_category, value):
    # find the transaction ID by its category
    response = requests.get(URL + "/api/transactions")
    transactions = response.json()
    t_id = None
    for t in transactions:
        if t["category"] == old_category:
            t_id = t["transaction_id"]
            break
            
    assert t_id is not None, f"Transaction with category {old_category} not found"

    # perform the update using the found ID
    json_body = { f"{field}": value }
    response = requests.patch(URL + f"/api/transactions/{t_id}", json=json_body)
    assert response.status_code == 200

@then('Transaction with category "{category}" exists in registry')
def check_transaction_exists(context, category):
    response = requests.get(URL + "/api/transactions")
    transactions = response.json()
    # check if any transaction has the requested category
    found = any(t["category"] == category for t in transactions)
    assert found is True

@when('I delete transaction with category: "{category}"')
def delete_transaction(context, category):
    # find ID
    response = requests.get(URL + "/api/transactions")
    transactions = response.json()
    t_id = None
    for t in transactions:
        if t["category"] == category:
            t_id = t["transaction_id"]
            break
            
    assert t_id is not None
    
    response = requests.delete(URL + f"/api/transactions/{t_id}")
    assert response.status_code == 200

@then('The account balance should be "{expected_balance}"')
def check_balance(context, expected_balance):
    response = requests.get(URL + "/api/summary")
    assert response.status_code == 200
    assert response.json()["balance"] == float(expected_balance)

@then('The budget status should be "{expected_status}"')
def check_budget_status(context, expected_status):
    response = requests.get(URL + "/api/summary")
    assert response.json()["budget_status"] == expected_status

@then('I cannot create a transaction with amount: "{amount}", category: "{category}"')
def try_create_invalid_transaction(context, amount, category):
    json_body = { 
        "amount": float(amount),
        "category": category,
        "date": "2026-01-24"
    }
    response = requests.post(URL + "/api/transactions", json=json_body)
    assert response.status_code == 422