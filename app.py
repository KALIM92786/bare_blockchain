from flask import Flask, jsonify, request, render_template
from blockchain import Blockchain, Token
import logging
import os
import json
from flask_cors import CORS

# Configure logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app)

# Initialize blockchain
blockchain = Blockchain()

# Blockchain state file
BLOCKCHAIN_FILE = "blockchain.json"

# Helper function to save blockchain state
def save_blockchain():
    with open(BLOCKCHAIN_FILE, "w") as f:
        data = {
            "chain": blockchain.chain,
            "current_transactions": blockchain.current_transactions,
            "tokens": [
                {
                    "name": token.name,
                    "symbol": token.symbol,
                    "total_supply": token.total_supply,
                    "balances": token.balances
                } for token in blockchain.tokens
            ]
        }
        json.dump(data, f, indent=4)

# Helper function to load blockchain state
def load_blockchain():
    if os.path.exists(BLOCKCHAIN_FILE):
        with open(BLOCKCHAIN_FILE, "r") as f:
            data = json.load(f)
            blockchain.chain = data.get("chain", [])
            blockchain.current_transactions = data.get("current_transactions", [])
            blockchain.tokens = [
                Token(
                    token_data["name"],
                    token_data["symbol"],
                    token_data["total_supply"]
                ) for token_data in data.get("tokens", [])
            ]
            for token, token_data in zip(blockchain.tokens, data.get("tokens", [])):
                token.balances = token_data["balances"]

# Load blockchain state on startup
load_blockchain()

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/explorer")
def explorer():
    return render_template('explorer.html')

@app.route("/new_block", methods=["GET"])
def new_block():
    try:
        previous_hash = blockchain.hash(blockchain.last_block)
        block = blockchain.new_block(previous_hash=previous_hash)
        response = {
            "message": "New Block Created",
            "index": block["index"],
            "transactions": block["transactions"],
            "validator": block["validator"],
            "previous_hash": block["previous_hash"],
        }
        save_blockchain()
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/transactions/new", methods=["POST"])
def new_transaction():
    values = request.get_json()
    required = ["sender", "recipient", "amount", "signature", "public_key", "metadata"]
    if not all(k in values for k in required):
        return jsonify({"error": "Missing values"}), 400
    try:
        index = blockchain.new_transaction(
            values["sender"], values["recipient"], values["amount"],
            values["signature"], values["public_key"], values.get("metadata")
        )
        save_blockchain()
        return jsonify({"message": f"Transaction will be added to Block {index}"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route("/chain", methods=["GET"])
def full_chain():
    response = {
        "chain": blockchain.chain,
        "length": len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route("/nodes/register", methods=["POST"])
def register_nodes():
    values = request.get_json()
    nodes = values.get("nodes")
    if nodes is None:
        return jsonify({"error": "Please supply a valid list of nodes"}), 400
    for node in nodes:
        blockchain.nodes.add(node)
    save_blockchain()
    return jsonify({"message": "New nodes have been added", "total_nodes": list(blockchain.nodes)}), 201

@app.route("/nodes/resolve", methods=["GET"])
def resolve_conflicts():
    # For simplicity, we are returning the current chain.
    response = {"message": "Current chain", "chain": blockchain.chain}
    save_blockchain()
    return jsonify(response), 200

@app.route("/smart-contract/deploy", methods=["POST"])
def deploy_contract():
    values = request.get_json()
    contract_id = values.get("contract_id")
    contract_code = values.get("contract_code")
    if not contract_id or not contract_code:
        return jsonify({"error": "Missing contract_id or contract_code"}), 400
    blockchain.deploy_smart_contract(contract_id, contract_code)
    save_blockchain()
    return jsonify({"message": f"Smart contract {contract_id} deployed successfully"}), 200

@app.route("/smart-contract/execute", methods=["POST"])
def execute_contract():
    values = request.get_json()
    contract_id = values.get("contract_id")
    method = values.get("method")
    args = values.get("args", {})
    if not contract_id or not method:
        return jsonify({"error": "Missing contract_id or method"}), 400
    try:
        result = blockchain.execute_contract(contract_id, method, args)
        return jsonify({"result": result}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route("/stake", methods=["POST"])
def stake():
    values = request.get_json()
    user = values.get("user")
    amount = values.get("amount")
    if not user or amount is None:
        return jsonify({"error": "Missing user or amount"}), 400
    try:
        response = blockchain.stake_tokens(user, amount)
        save_blockchain()
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# New endpoint to view current stakes
@app.route("/stakes", methods=["GET"])
def get_stakes():
    return jsonify({"stakes": blockchain.stakes}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
