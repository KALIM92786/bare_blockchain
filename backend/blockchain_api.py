from flask import Flask, jsonify, request
from blockchain import Blockchain
from functools import wraps
import jwt
import datetime
from werkzeug.security import check_password_hash
import logging

app = Flask(__name__)
blockchain = Blockchain()

# Configure secret key
app.config['SECRET_KEY'] = 'your_secret_key_here'
logging.basicConfig(level=logging.INFO)

# Dummy user credentials
users = {
    "admin": "hashed_password_here"
}

# Token Required Decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['username']
        except Exception as e:
            return jsonify({'message': f'Token is invalid! {str(e)}'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

# Login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required!'}), 400

    # Check credentials
    if username not in users or not check_password_hash(users[username], password):
        return jsonify({'message': 'Invalid credentials!'}), 401

    # Generate JWT
    token = jwt.encode(
        {'username': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
        app.config['SECRET_KEY'], algorithm="HS256"
    )
    return jsonify({'token': token}), 200

# Mine a new block
@app.route('/mine', methods=['GET'])
@token_required
def mine(current_user):
    try:
        last_proof = blockchain.last_block['proof']
        proof = blockchain.proof_of_work(last_proof)
        blockchain.new_transaction(sender="0", recipient=current_user, amount=1)
        block = blockchain.new_block(proof)
        logging.info(f"User {current_user} mined a block: {block}")
        return jsonify(block), 200
    except Exception as e:
        logging.error(f"Error in mining: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Add a new transaction
@app.route('/transactions/new', methods=['POST'])
@token_required
def new_transaction(current_user):
    try:
        values = request.get_json()
        required = ['sender', 'recipient', 'amount', 'signature', 'public_key']
        if not all(k in values for k in required):
            return 'Missing values', 400
        index = blockchain.new_transaction(
            values['sender'], values['recipient'], values['amount'],
            values['signature'], values['public_key']
        )
        return jsonify({'message': f'Transaction will be added to Block {index}'}), 201
    except Exception as e:
        logging.error(f"Error in transaction: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Other endpoints (chain, register nodes, resolve conflicts) remain similar...
