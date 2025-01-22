from flask import Flask, jsonify, request
from blockchain import Blockchain
from blockchain import Token
import logging
import os
import json
from flask_cors import CORS

# Configure logging
logging.basicConfig(level=logging.INFO)

# Create Flask app and enable CORS
app = Flask(__name__)
CORS(app)

# Initialize blockchain
blockchain = Blockchain()

# Load blockchain state from file
BLOCKCHAIN_FILE = "blockchain.json"

if os.path.exists(BLOCKCHAIN_FILE):
    with open(BLOCKCHAIN_FILE, "r") as f:
        data = json.load(f)
        blockchain.chain = data.get("chain", [])
        blockchain.current_transactions = data.get("current_transactions", [])
        blockchain.tokens = data.get("tokens", [])

# Save blockchain state to file
def save_blockchain():
    with open(BLOCKCHAIN_FILE, "w") as f:
        data = {
            "chain": blockchain.chain,
            "current_transactions": blockchain.current_transactions,
            "tokens": blockchain.tokens
        }
        json.dump(data, f)

@app.route('/')
def index():
    return "Welcome to the Blockchain API!"

@app.route('/mine', methods=['GET'])
def mine():
    last_proof = blockchain.last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    blockchain.new_transaction(
        sender="0",
        recipient="miner_address",
        amount=1,
        signature="dummy_signature",
        public_key="dummy_public_key"
    )

    block = blockchain.new_block(proof)
    save_blockchain()  # Save state after mining a block
    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    required = ['sender', 'recipient', 'amount', 'signature', 'public_key', 'metadata']
    if not all(k in values for k in required):
        return jsonify({'error': 'Missing values'}), 400

    try:
        index = blockchain.new_transaction(
            values['sender'], values['recipient'], values['amount'],
            values['signature'], values['public_key'], values.get('metadata')
        )
        save_blockchain()  # Save state after adding a transaction
        return jsonify({'message': f'Transaction will be added to Block {index}'}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()
    nodes = values.get('nodes')
    if nodes is None:
        return jsonify({'error': 'Please supply a valid list of nodes'}), 400

    for node in nodes:
        blockchain.register_node(node)

    save_blockchain()  # Save state after registering nodes
    return jsonify({'message': 'New nodes have been added', 'total_nodes': list(blockchain.nodes)}), 201

@app.route('/nodes/resolve', methods=['GET'])
def resolve_conflicts():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {'message': 'Our chain was replaced', 'new_chain': blockchain.chain}
    else:
        response = {'message': 'Our chain is authoritative', 'chain': blockchain.chain}

    save_blockchain()  # Save state after resolving conflicts
    return jsonify(response), 200

@app.route('/smart-contract/deploy', methods=['POST'])
def deploy_contract():
    values = request.get_json()
    contract_id = values.get('contract_id')
    contract_code = values.get('contract_code')

    if not contract_id or not contract_code:
        return jsonify({'error': 'Missing contract_id or contract_code'}), 400

    blockchain.deploy_smart_contract(contract_id, contract_code)
    save_blockchain()  # Save state after deploying a contract
    return jsonify({'message': f'Smart contract {contract_id} deployed successfully'}), 200

@app.route('/smart-contract/execute', methods=['POST'])
def execute_contract():
    values = request.get_json()
    contract_id = values.get('contract_id')
    method = values.get('method')
    args = values.get('args', {})

    if not contract_id or not method:
        return jsonify({'error': 'Missing contract_id or method'}), 400

    try:
        result = blockchain.execute_contract(contract_id, method, args)
        return jsonify({'result': result}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/transactions/analyze', methods=['GET'])
def analyze_transactions():
    suspicious = blockchain.analyze_transactions()
    return jsonify({'suspicious_transactions': suspicious}), 200

@app.route('/tokens/create', methods=['POST'])
def create_token():
    values = request.get_json()
    required = ['name', 'symbol', 'supply']
    if not all(k in values for k in required):
        return jsonify({'error': 'Missing values'}), 400

    # Check for duplicate token symbol
    for token in blockchain.tokens:
        if token['symbol'] == values['symbol']:
            return jsonify({'error': f"Token with symbol {values['symbol']} already exists."}), 400

    token = Token(values['name'], values['symbol'], values['supply'])
    blockchain.tokens.append({
        "name": token.name,
        "symbol": token.symbol,
        "total_supply": token.total_supply,
        "balances": token.balances
    })
    save_blockchain()
    return jsonify({'message': f"Token {token.name} created with total supply {token.total_supply}"}), 201

@app.route('/tokens/transfer', methods=['POST'])
def transfer_token():
    values = request.get_json()
    required = ['sender', 'recipient', 'amount', 'token_symbol']
    if not all(k in values for k in required):
        return jsonify({'error': 'Missing values'}), 400

    try:
        token_data = next(t for t in blockchain.tokens if t['symbol'] == values['token_symbol'])
        token = Token(token_data['name'], token_data['symbol'], token_data['total_supply'])
        token.balances = token_data['balances']

        blockchain.new_token_transaction(values['sender'], values['recipient'], values['amount'], token)
        token_data['balances'] = token.balances  # Update balances in the persistent data
        save_blockchain()  # Save state after transferring tokens
        return jsonify({'message': f"{values['amount']} {token.symbol} transferred from {values['sender']} to {values['recipient']}"}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except StopIteration:
        return jsonify({'error': 'Token not found'}), 404


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
