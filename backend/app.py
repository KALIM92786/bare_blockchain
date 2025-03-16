import os
import sys
# Add the parent directory to PYTHONPATH to locate other modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, jsonify, request, render_template
from blockchain import Blockchain, Token, Wallet
from urllib.parse import urlparse
import logging
import json
from dotenv import load_dotenv
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.backends import default_backend
from web3 import Web3
from validator_expansion import Blockchain as ExtendedBlockchain
from execution_layer.vm_manager import VMManager
# Import GovernanceProposal (make sure governance/__init__.py exists)
from governance.governance import GovernanceProposal

# Create the Flask app and enable CORS and Socket.IO
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Instantiate the VM Manager after the app is created
vm_manager = VMManager()

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY", "default_api_key")

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load private key at startup (for signing transactions)
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

# Instantiate the Blockchain
blockchain = Blockchain()

# Connect to Ethereum via Alchemy (or use WEB3_PROVIDER_URL from .env)
alchemy_url = os.getenv("WEB3_PROVIDER_URL", "https://eth-mainnet.g.alchemy.com/v2/IIrjVj4cyzUBZNrNVwbuMexxWbcrecKd")
w3 = Web3(Web3.HTTPProvider(alchemy_url))
if w3.is_connected():
    logging.info("✅ Successfully connected to Ethereum mainnet via Alchemy!")
else:
    logging.error("❌ Connection to Ethereum via Alchemy failed")

latest_block = w3.eth.block_number
logging.info(f"Latest Ethereum Block: {latest_block}")

# Function to load ABI from a file
def load_abi(filename):
    with open(filename) as f:
        data = json.load(f)
        return data.get("abi", data)

# Load contract ABIs and addresses (ensure addresses are in checksum format)
barecoin_abi = load_abi("barecoin_abi.json")
barecoin_address = Web3.to_checksum_address("0xf5c3F19c46C2f64761b1d905C59Bc95E8ad839A1")
barecoin_contract = w3.eth.contract(address=barecoin_address, abi=barecoin_abi)

staking_abi = load_abi("staking_governance_abi.json")
staking_address = Web3.to_checksum_address("0xe55156B28dEBaCC01178950186FE08868D7Fd961")
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
# VM Execution Endpoint
# ---------------------------
@app.route("/vm/execute", methods=["POST"])
def execute_vm():
    data = request.get_json()
    vm_type = data.get("vm_type")
    params = data.get("params", [])
    
    if not vm_type:
        return jsonify({"error": "Missing vm_type parameter"}), 400
    
    try:
        result = vm_manager.execute_code(vm_type, *params)
        return jsonify({"result": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------------------
# AI Analysis Endpoint
# ---------------------------
@app.route("/ai/analyze", methods=["POST"])
def analyze_transaction():
    """
    Expects JSON payload with a "transaction" key.
    Example:
    {
      "transaction": {
          "sender": "0x123...",
          "recipient": "0xabc...",
          "amount": 500,
          "metadata": {}
      }
    }
    """
    data = request.get_json()
    transaction = data.get("transaction")
    if not transaction:
        return jsonify({"error": "Missing transaction data"}), 400
    try:
        from execution_layer.ai_module import AI_Module
        ai = AI_Module()
        analysis = ai.analyze_transaction(transaction)
        return jsonify({"analysis": analysis}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------------------
# Governance Endpoints
# ---------------------------
@app.route("/governance/propose", methods=["POST"])
@require_api_key
def propose():
    """
    Submit a new governance proposal.
    Expects JSON payload:
    {
      "proposal_id": "unique_id",
      "description": "Description of the proposal",
      "proposer": "0xYourAddress"
    }
    """
    data = request.get_json()
    proposal_id = data.get("proposal_id")
    description = data.get("description")
    proposer = data.get("proposer")
    if not proposal_id or not description or not proposer:
        return jsonify({"error": "Missing proposal_id, description, or proposer"}), 400
    try:
        # Create a new proposal using GovernanceProposal class (implementation to be defined)
        proposal = GovernanceProposal(proposal_id, description, proposer)
        # Store the proposal in the blockchain governance store (or use a database)
        if not hasattr(blockchain, "governance"):
            blockchain.governance = {}
        blockchain.governance[proposal_id] = proposal.to_dict()  # Ensure GovernanceProposal has a to_dict() method
        return jsonify({"message": "Proposal submitted successfully", "proposal": blockchain.governance[proposal_id]}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/governance/vote", methods=["POST"])
@require_api_key
def vote():
    """
    Cast a vote on an existing proposal.
    Expects JSON payload:
    {
      "proposal_id": "unique_id",
      "voter": "0xYourAddress",
      "vote": "yes"  // or "no"
    }
    """
    data = request.get_json()
    proposal_id = data.get("proposal_id")
    voter = data.get("voter")
    vote_value = data.get("vote")
    if not proposal_id or not voter or vote_value not in ["yes", "no"]:
        return jsonify({"error": "Missing or invalid proposal_id, voter, or vote value"}), 400
    try:
        if not hasattr(blockchain, "governance") or proposal_id not in blockchain.governance:
            return jsonify({"error": "Proposal not found"}), 404
        blockchain.governance[proposal_id]["votes"][voter] = vote_value
        return jsonify({"message": "Vote recorded", "proposal": blockchain.governance[proposal_id]}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/governance/results", methods=["GET"])
def governance_results():
    """
    Retrieve the current governance proposals and their vote counts.
    """
    try:
        if not hasattr(blockchain, "governance"):
            return jsonify({"message": "No proposals found"}), 200
        return jsonify({"governance": blockchain.governance}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------------------
# Smart Contract Endpoints
# ---------------------------
@app.route("/smart-contract/deploy", methods=["POST"])
@require_api_key
def deploy_contract():
    values = request.get_json()
    contract_id = values.get("contract_id")
    contract_code = values.get("contract_code")
    if not contract_id or not contract_code:
        return jsonify({"error": "Missing contract_id or contract_code"}), 400
    try:
        blockchain.deploy_smart_contract(contract_id, contract_code)
        return jsonify({"message": f"Smart contract {contract_id} deployed successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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
    except Exception as e:
        return jsonify({"error": str(e)}), 400

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
        # Emit new block event via Socket.IO
        socketio.emit("new_block", response)
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

# Additional endpoints
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
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
