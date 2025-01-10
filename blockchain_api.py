from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from blockchain import Blockchain
import jwt
import datetime
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, static_url_path='', static_folder='static')
CORS(app)
blockchain = Blockchain()

# Secret key for encoding JWT
app.config['SECRET_KEY'] = 'your_secret_key_here'

# User credentials (hardcoded for simplicity, ideally stored in a database)
users = {
    "admin": generate_password_hash("password123")
}

# Utility: Token Required Decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['username']
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

# Login endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username not in users or not check_password_hash(users[username], password):
        return jsonify({'message': 'Invalid credentials!'}), 401

    token = jwt.encode(
        {'username': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
        app.config['SECRET_KEY'],
        algorithm="HS256"
    )
    return jsonify({'token': token})

# Mine a new block (secured)
@app.route('/mine', methods=['GET'])
@token_required
def mine(current_user):
    last_proof = blockchain.last_block['proof']
    proof = blockchain.proof_of_work(last_proof)
    blockchain.new_transaction(sender="0", recipient="miner_address", amount=1)
    block = blockchain.new_block(proof)
    return jsonify(block), 200

# Add a new transaction (secured)
@app.route('/transactions/new', methods=['POST'])
@token_required
def new_transaction(current_user):
    values = request.get_json()
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
    return jsonify({'message': f'Transaction will be added to Block {index}'}), 201

# Return the full blockchain (secured)
@app.route('/chain', methods=['GET'])
@token_required
def full_chain(current_user):
    return jsonify({'chain': blockchain.chain, 'length': len(blockchain.chain)}), 200

# Register new nodes (secured)
@app.route('/nodes/register', methods=['POST'])
@token_required
def register_nodes(current_user):
    values = request.get_json()
    nodes = values.get('nodes')

    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    return jsonify({
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }), 201

# Resolve conflicts (secured)
@app.route('/nodes/resolve', methods=['GET'])
@token_required
def consensus(current_user):
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
