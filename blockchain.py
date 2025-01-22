import os
import json
import hashlib
import sqlite3
from time import time
from urllib.parse import urlparse
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
import logging
import base64
import subprocess

# Configure logging
logging.basicConfig(level=logging.INFO)

DATABASE_FILE = "blockchain.db"
tokens = []  # Global tokens list


class Blockchain:
    def __init__(self):
        global tokens  # Ensure tokens is accessible
        self.chain = []
        self.current_transactions = []
        self.nodes = set()
        self.smart_contracts = {}

        # Database initialization
        self.db = sqlite3.connect(DATABASE_FILE)
        self.initialize_database()
        self.load_data()

        # Ensure at least one block exists
        if not self.chain:
            self.new_block(previous_hash="1", proof=100)

    def initialize_database(self):
        cursor = self.db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS blockchain (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chain TEXT,
                current_transactions TEXT,
                tokens TEXT
            )
        ''')
        self.db.commit()

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
        self.save_data()
        return block

    def new_transaction(self, sender, recipient, amount, signature, public_key, metadata=None):
        if not Wallet.verify_signature(public_key, f"{sender}{amount}{recipient}", signature):
            raise ValueError("Invalid signature")

        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
            'timestamp': time(),
            'metadata': metadata or {}
        }
        self.current_transactions.append(transaction)
        self.save_data()
        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

    def save_data(self):
        global tokens
        cursor = self.db.cursor()
        data = {
            'chain': json.dumps(self.chain),
            'current_transactions': json.dumps(self.current_transactions),
            'tokens': json.dumps([
                {
                    'name': token.name,
                    'symbol': token.symbol,
                    'total_supply': token.total_supply,
                    'balances': token.balances
                } for token in tokens
            ])
        }
        cursor.execute("DELETE FROM blockchain")
        cursor.execute("INSERT INTO blockchain (chain, current_transactions, tokens) VALUES (?, ?, ?)",
                       (data['chain'], data['current_transactions'], data['tokens']))
        self.db.commit()

    def load_data(self):
        global tokens
        cursor = self.db.cursor()
        cursor.execute("SELECT chain, current_transactions, tokens FROM blockchain")
        row = cursor.fetchone()
        if row:
            self.chain = json.loads(row[0])
            self.current_transactions = json.loads(row[1])
            tokens = []  # Reinitialize tokens list
            for token_data in json.loads(row[2]):
                token = Token(token_data['name'], token_data['symbol'], token_data['total_supply'])
                token.balances = token_data['balances']
                tokens.append(token)
        else:
            logging.info("No data in the database. Starting fresh.")

    def analyze_transactions(self, threshold=10000):
        """
        Analyzes transactions to find suspicious ones exceeding the given threshold.
        """
        suspicious_transactions = [
            tx for block in self.chain for tx in block['transactions'] if tx['amount'] > threshold
        ]
        return suspicious_transactions

    def proof_of_work(self, last_proof):
        """
        Proof of Work algorithm: Increment proof until valid hash is found.
        """
        proof = 0
        while not self.valid_proof(last_proof, proof):
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates the proof: Does hash(last_proof, proof) contain 4 leading zeros?
        """
        guess = f"{last_proof}{proof}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def deploy_smart_contract(self, contract_id, contract_code):
        """
        Deploy a new smart contract with an ID and code.
        """
        self.smart_contracts[contract_id] = contract_code
        return True


# Wallet and Token classes remain unchanged
class Wallet:
    @staticmethod
    def generate_keys():
        private_key = rsa.generate_private_key(
            public_exponent=65537, key_size=2048, backend=default_backend()
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


class Token:
    def __init__(self, name, symbol, initial_supply):
        self.name = name
        self.symbol = symbol
        self.total_supply = initial_supply
        self.balances = {"admin": initial_supply}  # Initialize balances

    def transfer(self, sender, recipient, amount):
        sender_balance = int(self.balances.get(sender, 0))
        if sender_balance < amount:
            raise ValueError("Insufficient balance.")
        self.balances[sender] = sender_balance - amount
        self.balances[recipient] = int(self.balances.get(recipient, 0)) + amount


private_key, public_key = Wallet.generate_keys()
logging.info(f"Private Key:\n{private_key}")
logging.info(f"Public Key:\n{public_key}")

