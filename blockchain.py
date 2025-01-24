import os
import json
import hashlib
import logging
import sqlite3
import cloudinary
import cloudinary.uploader
from time import time
from urllib.parse import urlparse
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
from sklearn.ensemble import IsolationForest
import base64
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)

DATABASE_FILE = "blockchain.db"
CLOUDINARY_FOLDER = "blockchain-backup"

# Configure Cloudinary
cloudinary.config(
    cloud_name="your-cloud-name",
    api_key="your-api-key",
    api_secret="your-api-secret"
)


class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.tokens = []
        self.nodes = set()
        self.smart_contracts = {}
        self.db = sqlite3.connect(DATABASE_FILE)
        self.initialize_database()
        self.load_data()

        if not self.chain:
            self.new_block(previous_hash="1", proof=100)

    def initialize_database(self):
        cursor = self.db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS blockchain (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chain TEXT,
                current_transactions TEXT,
                tokens TEXT
            )
        """)
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
        self.backup_to_cloud()
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

    def analyze_transactions_with_ai(self):
        transactions = [
            [tx["amount"], tx.get("metadata", {}).get("risk_score", 0)]
            for block in self.chain for tx in block["transactions"]
        ]
        if not transactions:
            return []

        model = IsolationForest(contamination=0.05)
        model.fit(transactions)

        anomalies = [
            block["transactions"][i]
            for block in self.chain
            for i, tx in enumerate(block["transactions"])
            if model.predict([[tx["amount"], tx.get("metadata", {}).get("risk_score", 0)]]) == -1
        ]
        return anomalies

    def deploy_smart_contract(self, contract_id, contract_code):
        self.smart_contracts[contract_id] = contract_code
        return True

    def execute_contract(self, contract_id, method, args):
        if contract_id not in self.smart_contracts:
            raise ValueError("Contract not found")
        contract_code = self.smart_contracts[contract_id]
        exec(contract_code, globals())
        return eval(f"{method}(**args)")

    def save_data(self):
        cursor = self.db.cursor()
        data = {
            'chain': json.dumps(self.chain),
            'current_transactions': json.dumps(self.current_transactions),
            'tokens': json.dumps([{
                'name': token.name,
                'symbol': token.symbol,
                'total_supply': token.total_supply,
                'balances': token.balances
            } for token in self.tokens])
        }
        cursor.execute("DELETE FROM blockchain")
        cursor.execute("INSERT INTO blockchain (chain, current_transactions, tokens) VALUES (?, ?, ?)",
                       (data['chain'], data['current_transactions'], data['tokens']))
        self.db.commit()

    def load_data(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT chain, current_transactions, tokens FROM blockchain")
        row = cursor.fetchone()
        if row:
            self.chain = json.loads(row[0])
            self.current_transactions = json.loads(row[1])
            self.tokens = [Token.from_dict(json.loads(token)) for token in json.loads(row[2])]
        else:
            logging.info("No data found, starting fresh.")

    def backup_to_cloud(self):
        data = {
            "chain": self.chain,
            "current_transactions": self.current_transactions,
            "tokens": [token.to_dict() for token in self.tokens]
        }
        backup_json = json.dumps(data, indent=4)
        response = cloudinary.uploader.upload(
            backup_json,
            resource_type="raw",
            folder=CLOUDINARY_FOLDER,
            public_id=f"blockchain_backup_{int(time())}"
        )
        logging.info(f"Blockchain backed up to cloud: {response.get('secure_url')}")

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]


class Token:
    def __init__(self, name, symbol, total_supply):
        self.name = name
        self.symbol = symbol
        self.total_supply = total_supply
        self.balances = {"admin": total_supply}

    def transfer(self, sender, recipient, amount):
        if self.balances.get(sender, 0) < amount:
            raise ValueError("Insufficient balance")
        self.balances[sender] -= amount
        self.balances[recipient] = self.balances.get(recipient, 0) + amount

    def to_dict(self):
        return {
            "name": self.name,
            "symbol": self.symbol,
            "total_supply": self.total_supply,
            "balances": self.balances,
        }

    @staticmethod
    def from_dict(data):
        token = Token(data["name"], data["symbol"], data["total_supply"])
        token.balances = data["balances"]
        return token


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


# Generate test keys
private_key, public_key = Wallet.generate_keys()
logging.info(f"Private Key:\n{private_key}")
logging.info(f"Public Key:\n{public_key}")
