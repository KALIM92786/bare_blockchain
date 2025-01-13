from flask import Flask, jsonify, request
from blockchain import Blockchain
import logging
import sys
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from flask_cors import CORS
CORS(app)
import os
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")



# Configure logging
logging.basicConfig(level=logging.INFO)

# Load private key
try:
    with open("private_key.pem", "rb") as key_file:
        private_key = load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend(),
        )
    logging.info("Private key loaded successfully.")
except Exception as e:
    logging.error(f"Error loading private key: {e}")

# Load public key
try:
    with open("public_key.pem", "rb") as key_file:
        public_key = load_pem_public_key(
            key_file.read(),
            backend=default_backend(),
        )
    logging.info("Public key loaded successfully.")
except Exception as e:
    logging.error(f"Error loading public key: {e}")

# Create Flask app and blockchain
app = Flask(__name__)
blockchain = Blockchain()


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
    required = ['sender', 'recipient', 'amount', 'signature', 'public_key']
    if not all(k in values for k in required):
        return jsonify({'error': 'Missing values'}), 400

    try:
        index = blockchain.new_transaction(
            values['sender'], values['recipient'], values['amount'],
            values['signature'], values['public_key']
        )
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

    return jsonify({'message': 'New nodes have been added', 'total_nodes': list(blockchain.nodes)}), 201


@app.route('/nodes/resolve', methods=['GET'])
def resolve_conflicts():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {'message': 'Our chain was replaced', 'new_chain': blockchain.chain}
    else:
        response = {'message': 'Our chain is authoritative', 'chain': blockchain.chain}
    return jsonify(response), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
