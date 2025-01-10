from flask import Flask, jsonify, request
from blockchain import Blockchain
from urllib.parse import urlparse

from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to the Bare Blockchain API!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)


# Instantiate the Blockchain
blockchain = Blockchain()

# List of nodes
nodes = set()

@app.route('/mine', methods=['GET'])
def mine():
    """
    Mines a new block by finding the proof of work
    """
    try:
        print("Starting mining process...")  # Debug log
        last_proof = blockchain.last_block['proof']
        print(f"Last proof: {last_proof}")  # Debug log
        
        proof = blockchain.proof_of_work(last_proof)
        print(f"New proof: {proof}")  # Debug log

        # The sender is "0" to signify that this node has mined a new coin
        blockchain.new_transaction(
            sender="0",
            recipient="your_address",  # Replace "your_address" with your actual address
            amount=1,
        )

        block = blockchain.new_block(proof)
        print(f"New block created: {block}")  # Debug log

        response = {
            'message': "New Block Forged",
            'index': block['index'],
            'transactions': block['transactions'],
            'proof': block['proof'],
            'previous_hash': block['previous_hash'],
        }
        return jsonify(response), 200
    except Exception as e:
        print(f"Error in /mine: {str(e)}")  # Log the error to console
        return jsonify({'error': str(e)}), 500

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    """
    Creates a new transaction
    """
    try:
        values = request.get_json()
        print(f"Received transaction data: {values}")  # Debug input data

        # Check that the required fields are in the POSTed data
        required = ['sender', 'recipient', 'amount']
        if not values or not all(k in values for k in required):
            return jsonify({'error': 'Missing values'}), 400

        # Create a new transaction
        index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
        response = {'message': f'Transaction will be added to Block {index}'}
        return jsonify(response), 201
    except Exception as e:
        print(f"Error in /transactions/new: {str(e)}")  # Log the error
        return jsonify({'error': str(e)}), 500

@app.route('/chain', methods=['GET'])
def full_chain():
    """
    Returns the full blockchain
    """
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    """
    Register new nodes to the blockchain network
    """
    values = request.get_json()

    nodes_to_register = values.get('nodes')

    if nodes_to_register is None:
        return jsonify({'error': 'Please supply a list of nodes'}), 400

    for node in nodes_to_register:
        parsed_url = urlparse(node)
        if parsed_url.netloc:
            nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            nodes.add(parsed_url.path)
        else:
            return jsonify({'error': 'Invalid URL'}), 400

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(nodes)
    }
    return jsonify(response), 201

@app.route('/nodes/resolve', methods=['GET'])
def resolve_conflicts():
    """
    Resolves conflicts by replacing the chain with the longest one in the network
    """
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
