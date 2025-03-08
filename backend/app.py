from flask import Flask, jsonify, request, render_template
from blockchain import Blockchain, Token, Wallet
from urllib.parse import urlparse
import logging
import sys
import json
import os
from dotenv import load_dotenv
from flask_cors import CORS
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.backends import default_backend
from web3 import Web3
from validator_expansion import Blockchain as ExtendedBlockchain

# Ensure the current directory is in the module search path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Load environment variables (ensure .env contains API_KEY, PRIVATE_KEY, etc.)
load_dotenv()
API_KEY = os.getenv("API_KEY", "default_api_key")

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load private key at startup (for signing transactions, if needed)
private_key_path = "private_key.pem"
private_key_data = None
if os.path.exists(private_key_path):
    with open(private_key_path, "rb") as key_file:
        private_key_data = key_file.read()
else:
    env_key = os.environ.get("PRIVATE_KEY")
    if env_key:
        private_key_data = env_key.encode()
    else:
        logging.error("Error loading private key: No 'private_key.pem' file found and PRIVATE_KEY environment variable is not set.")
        sys.exit(1)

try:
    private_key = load_pem_private_key(
        private_key_data,
        password=None,
        backend=default_backend()
    )
except Exception as e:
    logging.error(f"Error loading private key: {e}")
    sys.exit(1)

app = Flask(__name__)
CORS(app)

# Instantiate the Blockchain
blockchain = Blockchain()

# Connect to Ethereum via Alchemy
alchemy_url = "https://eth-mainnet.g.alchemy.com/v2/IIrjVj4cyzUBZNrNVwbuMexxWbcrecKd"
w3 = Web3(Web3.HTTPProvider(alchemy_url))
if w3.is_connected():
    logging.info("✅ Successfully connected to Ethereum mainnet via Alchemy!")
else:
    logging.error("❌ Connection to Ethereum via Alchemy failed")

latest_block = w3.eth.block_number
logging.info(f"Latest Ethereum Block: {latest_block}")
# Optionally, print block details if needed:
# print(w3.eth.get_block(latest_block, full_transactions=True))

# Function to load ABI from a file
def load_abi(filename):
    with open(filename) as f:
        data = json.load(f)
        return data.get("abi", data)

# Load contract ABIs and addresses (update these addresses as needed)
barecoin_abi = load_abi("barecoin_abi.json")
barecoin_address = "0x5FbDB2315678afecb367f032d93F642f64180aa3"
barecoin_contract = w3.eth.contract(address=barecoin_address, abi=barecoin_abi)

staking_abi = load_abi("staking_governance_abi.json")
staking_address = "0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512"
staking_contract = w3.eth.contract(address=staking_address, abi=staking_abi)

# API key authentication decorator
def require_api_key(f):
    def decorated(*args, **kwargs):
        key = request.headers.get("x-api-key")
        if key != API_KEY:
            return jsonify({"error": "Unauthorized"}), 403
        return f(*args, **kwargs)
    decorated.__name__ = f.__name__
    return decorated

# Global error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Server error"}), 500

# Routes for rendering pages
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/explorer")
def explorer():
    return render_template('explorer.html')

# ---------------------------
# Blockchain API Endpoints
# ---------------------------
@app.route("/mine", methods=["GET"])
def mine():
    try:
        logging.info("Starting mining process...")
        last_proof = blockchain.last_block['proof']
        proof = blockchain.proof_of_work(last_proof)
        blockchain.new_transaction(
            sender="0",
            recipient="your_address",  # Update to actual reward recipient
            amount=1,
            signature="dummy_signature",
            public_key="dummy_public_key"
        )
        new_blk = blockchain.new_block(previous_hash=blockchain.hash(blockchain.last_block))
        response = {
            'message': "New Block Forged",
            'index': new_blk['index'],
            'transactions': new_blk['transactions'],
            'proof': new_blk['proof'],
            'previous_hash': new_blk['previous_hash'],
        }
        return jsonify(response), 200
    except Exception as e:
        logging.error(f"Error in /mine: {e}")
        return jsonify({'error': str(e)}), 500

@app.route("/transactions/new", methods=["POST"])
def new_transaction():
    values = request.get_json()
    required = ["sender", "recipient", "amount", "signature", "public_key"]
    if not all(k in values for k in required):
        return jsonify({"error": "Missing values"}), 400
    try:
        index = blockchain.new_transaction(
            values["sender"], values["recipient"], values["amount"],
            values["signature"], values["public_key"]
        )
        return jsonify({"message": f"Transaction will be added to Block {index}"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route("/chain", methods=["GET"])
def full_chain():
    return jsonify({"chain": blockchain.chain, "length": len(blockchain.chain)}), 200

@app.route("/nodes/register", methods=["POST"])
@require_api_key
def register_nodes():
    values = request.get_json()
    nodes = values.get("nodes")
    if nodes is None:
        return jsonify({"error": "Please supply a valid list of nodes"}), 400
    for node in nodes:
        blockchain.nodes.add(node)
    return jsonify({"message": "New nodes have been added", "total_nodes": list(blockchain.nodes)}), 201

@app.route("/nodes/resolve", methods=["GET"])
def resolve_conflicts():
    return jsonify({"message": "Current chain", "chain": blockchain.chain}), 200

# Smart Contract endpoints
@app.route("/smart-contract/deploy", methods=["POST"])
@require_api_key
def deploy_contract():
    values = request.get_json()
    contract_id = values.get("contract_id")
    contract_code = values.get("contract_code")
    if not contract_id or not contract_code:
        return jsonify({"error": "Missing contract_id or contract_code"}), 400
    blockchain.deploy_smart_contract(contract_id, contract_code)
    return jsonify({"message": f"Smart contract {contract_id} deployed successfully"}), 200

@app.route("/smart-contract/execute", methods=["POST"])
@require_api_key
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

# Additional useful endpoints

@app.route("/balance/<address>", methods=["GET"])
def get_balance(address):
    try:
        balance = barecoin_contract.functions.balanceOf(address).call()
        return jsonify({"balance": balance}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/staker/<address>", methods=["GET"])
def get_staker(address):
    try:
        staker = staking_contract.functions.stakers(address).call()
        return jsonify({"amount": staker[0], "reward": staker[1], "lastStaked": staker[2]}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/blockchain/stake_tokens", methods=["POST"])
@require_api_key
def stake_tokens():
    data = request.get_json()
    user = data.get("user")
    amount = data.get("amount")
    if not user or amount is None:
        return jsonify({"error": "Missing user or amount"}), 400
    try:
        result = blockchain.stake_tokens(user, int(amount))
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/transactions/pending", methods=["GET"])
def pending_transactions():
    try:
        transactions = blockchain.get_pending_transactions()
        return jsonify(transactions), 200
    except Exception as e:
        logging.error(f"Error in /transactions/pending: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
