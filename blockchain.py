import os
import json
import hashlib
import requests
from time import time
from urllib.parse import urlparse
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
import logging
import base64

logging.basicConfig(level=logging.INFO)

SECRET_KEY = "your_shared_secret_key"

# List to store all tokens
tokens = []

class Token:
    def __init__(self, name, symbol, initial_supply):
        self.name = name
        self.symbol = symbol
        self.total_supply = initial_supply
        self.balances = {}

        # Allocate the total supply to the creator
        self.balances["admin"] = initial_supply

    def transfer(self, sender, recipient, amount):
        if self.balances.get(sender, 0) < amount:
            raise ValueError("Insufficient balance")
        self.balances[sender] -= amount
        self.balances[recipient] = self.balances.get(recipient, 0) + amount


class Wallet:
    @staticmethod
    def generate_keys():
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()

        private_key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
        public_key_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        return private_key_pem.decode(), public_key_pem.decode()

    @staticmethod
    def sign_transaction(private_key_pem, transaction_data):
        private_key = serialization.load_pem_private_key(
            private_key_pem.encode(), password=None, backend=default_backend()
        )
        signature = private_key.sign(
            transaction_data.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return base64.b64encode(signature).decode()

    @staticmethod
    def verify_signature(public_key_pem, transaction_data, signature):
        public_key = serialization.load_pem_public_key(
            public_key_pem.encode(), backend=default_backend()
        )
        try:
            public_key.verify(
                base64.b64decode(signature.encode()),
                transaction_data.encode(),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception:
            return False


class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.nodes = set()
        self.smart_contracts = {}  # New for smart contracts
        
        # Load data from file
        self.load_data()
        
        # Ensure at least one block exists
        if not self.chain:
            self.new_block(previous_hash='1', proof=100)

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.current_transactions = []
        self.chain.append(block)
        self.save_data()  # Save blockchain state
        return block

    def new_transaction(self, sender, recipient, amount, signature, public_key, metadata=None):
        if not Wallet.verify_signature(public_key, f"{sender}{amount}{recipient}", signature):
            raise ValueError("Invalid signature")

        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
            'timestamp': time(),
            'metadata': metadata or {}  # Additional IoT metadata
        }
        self.current_transactions.append(transaction)
        self.save_data()  # Save blockchain state
        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        proof = 0
        while not self.valid_proof(last_proof, proof):
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f"{last_proof}{proof}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def register_node(self, address):
        parsed_url = urlparse(address)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError("Invalid URL")

    def new_token_transaction(self, sender, recipient, amount, token):
        if sender not in token.balances:
            raise ValueError("Sender does not own this token")
        token.transfer(sender, recipient, amount)

        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
            'token': token.symbol,
            'timestamp': time()
        })
        self.save_data()  # Save blockchain and token state
        return self.last_block['index'] + 1

    def deploy_smart_contract(self, contract_id, contract_code):
        self.smart_contracts[contract_id] = contract_code
        return True

    def execute_contract(self, contract_id, method, args):
        if contract_id not in self.smart_contracts:
            raise ValueError("Contract not found")
        contract = self.smart_contracts[contract_id]
        exec(contract, globals())  # Warning: Use a safe execution method in production!
        return eval(f"{method}(**args)")

    def analyze_transactions(self):
        suspicious_transactions = [
            tx for block in self.chain for tx in block['transactions'] if tx['amount'] > 10000
        ]
        return suspicious_transactions

    def save_data(self):
        """Save blockchain, current transactions, and tokens to a JSON file."""
        data = {
            'chain': self.chain,
            'current_transactions': self.current_transactions,
            'tokens': [
                {
                    'name': token.name,
                    'symbol': token.symbol,
                    'total_supply': token.total_supply,
                    'balances': token.balances
                } for token in tokens
            ]
        }
        with open('blockchain.json', 'w') as file:
            json.dump(data, file, indent=4)

    def load_data(self):
        """Load blockchain, current transactions, and tokens from a JSON file."""
        try:
            with open('blockchain.json', 'r') as file:
                data = json.load(file)
                self.chain = data.get('chain', [])
                self.current_transactions = data.get('current_transactions', [])
                
                global tokens
                tokens = [
                    Token(
                        token_data['name'],
                        token_data['symbol'],
                        token_data['total_supply']
                    ) for token_data in data.get('tokens', [])
                ]
                for token, token_data in zip(tokens, data.get('tokens', [])):
                    token.balances = token_data['balances']
        except FileNotFoundError:
            logging.info("No blockchain.json file found. Starting with a new blockchain.")


# Generate keys for testing
private_key, public_key = Wallet.generate_keys()
logging.info(f"Private Key:\n{private_key}")
logging.info(f"Public Key:\n{public_key}")
