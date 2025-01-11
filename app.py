from flask import Flask, jsonify, request
from blockchain import Blockchain
from urllib.parse import urlparse
import logging
import sys
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.backends import default_backend

# Load private key at the start of your app
try:
    with open("private_key.pem", "rb") as key_file:
        private_key = load_pem_private_key(
            key_file.read(),
            password=None,  # Replace 'None' with the password if your key is encrypted
            backend=default_backend()
        )
except (FileNotFoundError, ValueError) as e:
    logging.error(f"Error loading private key: {e}")
    sys.exit(1)

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Instantiate the Blockchain
blockchain = Blockchain()

@app.route('/')
def index():
    return "Welcome to the Bare Blockchain API!"

@app.route('/mine', methods=['GET'])
def mine():
    try:
        logging.info("Starting mining process...")
        last_proof = blockchain.last_block['proof']
        proof = blockchain.proof_of_work(last_proof)

        blockchain.new_transaction(
            sender="0",
            recipient="your_address",  # Replace with your actual address
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
    except Exception as e:
        logging.error(f"Error in /mine: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    try:
        index = blockchain.new_transaction(
            values['sender'], values['recipient'], values['amount'],
            values['signature'], values['public_key']
        )
        response = {'message': f'Transaction will be added to Block {index}'}
        return jsonify(response), 201
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
    nodes_to_register = values.get('nodes')

    if nodes_to_register is None:
        return jsonify({'error': 'Please supply a list of nodes'}), 400

    for node in nodes_to_register:
        parsed_url = urlparse(node)
        if parsed_url.netloc:
            blockchain.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            blockchain.nodes.add(parsed_url.path)
        else:
            return jsonify({'error': 'Invalid URL'}), 400

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes)
    }
    return jsonify(response), 201

@app.route('/nodes/resolve', methods=['GET'])
def resolve_conflicts():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {'message': 'Our chain was replaced', 'new_chain': blockchain.chain}
    else:
        response = {'message': 'Our chain is authoritative', 'chain': blockchain.chain}

    return jsonify(response), 200


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    app.run(host='0.0.0.0', port=port)
