from flask import Flask, request, jsonify
from src.finance_manager import FinanceManager
from src.user import User
from src.transaction import Transaction

app = Flask(__name__)

default_user = User("Alice", "alice@example.com", 25)
manager = FinanceManager(default_user)

@app.route("/api/transactions", methods=["POST"])
def add_transaction():
    data = request.get_json()
    print(f"Add transaction request: {data}")

    if not data or "amount" not in data or "category" not in data:
        return jsonify({"message": "Invalid body"}), 400

    new_transaction = Transaction(
        amount=data["amount"],
        category=data["category"],
        date=data.get("date")
    )

    if manager.add_transaction(new_transaction):
        return jsonify({"message": "Transaction added"}), 201
    return jsonify({"message": "Invalid transaction data"}), 422

@app.route("/api/transactions", methods=["GET"])
def get_history():
    print("Get transaction history request received")
    history = manager.get_history()
    output = [
        {
            "transaction_id": t.transaction_id,
            "amount": t.amount,
            "category": t.category,
            "type": t.type,
            "date": t.date
        } for t in history
    ]
    return jsonify(output), 200

@app.route("/api/summary", methods=["GET"])
def get_summary():
    print("Get summary request received")
    return jsonify({
        "user": manager.user.name,
        "balance": manager.get_balance(),
        "budget_status": manager.check_budget_status()
    }), 200

@app.route("/api/transactions/<t_id>", methods=["DELETE"])
def delete_transaction(t_id):
    print(f"Delete transaction request for ID: {t_id}")
    history = manager.get_history()
    
    for t in history:
        if t.transaction_id == t_id:
            history.remove(t)
            return jsonify({"message": "Transaction deleted"}), 200
            
    return jsonify({"message": "Transaction not found"}), 404

@app.route("/api/transactions/<t_id>", methods=["PATCH"])
def update_transaction(t_id):
    print(f"Update transaction request for ID: {t_id}")
    data = request.get_json()
    history = manager.get_history()

    for t in history:
        if t.transaction_id == t_id:
            if "category" in data:
                t.category = data["category"]
                t.type = t.assign_type(data["category"])
            return jsonify({"message": "Transaction updated"}), 200

    return jsonify({"message": "Transaction not found"}), 404