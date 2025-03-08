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
import base64
import tempfile
import random  # PoS validator selection
from validator_expansion import Blockchain as ExtendedBlockchain
import sys

# Set module search path to current directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(level=logging.INFO)

DATABASE_FILE = "blockchain.db"
CLOUDINARY_FOLDER = "blockchain-backup"

# Configure Cloudinary
cloudinary.config(
    cloud_name="dcktfwqkb",
    api_key="632313894921797",
    api_secret="5FYfjr3ysJgtG6tKFONyRzVLl-U"
)

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.tokens = []  # List of Token objects
        self.nodes = set()
        self.smart_contracts = {}
        self.stakes = {}  # Mapping of user to staked amount
        try:
            self.db = sqlite3.connect(DATABASE_FILE, check_same_thread=False)
            self.initialize_database()
            self.load_data()
        except Exception as e:
            logging.error(f"Database initialization error: {e}")
            self.chain = []
            self.current_transactions = []
            self.tokens = []
        # Create genesis block if chain is empty
        if not self.chain:
            self.new_block(previous_hash="1")

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
        logging.info("Database initialized successfully.")

    def stake_tokens(self, user, amount):
        try:
            self.stakes[user] = self.stakes.get(user, 0) + amount
            logging.info(f"{user} staked {amount} tokens.")
            return {"message": f"{user} staked {amount} tokens."}
        except Exception as e:
            logging.error(f"Error staking tokens for {user}: {e}")
            raise e

    def select_validator(self):
        if not self.stakes:
            raise ValueError("No stakes available; no validator can be selected.")
        total_stake = sum(self.stakes.values())
        pick = random.uniform(0, total_stake)
        current = 0
        for user, stake in self.stakes.items():
            current += stake
            if current >= pick:
                logging.info(f"Validator selected: {user}")
                return user
        logging.warning("Validator selection reached end without pick; defaulting to None")
        return None

    def new_block(self, previous_hash=None):
        try:
            validator = self.select_validator()
            if validator is None:
                raise ValueError("No validator available to create a block.")
            reward_transaction = {
                'sender': "0",
                'recipient': validator,
                'amount': 1,  # Staking reward
                'timestamp': time(),
                'metadata': {'reward': True}
            }
            self.current_transactions.append(reward_transaction)
            self.save_data()

            block = {
                'index': len(self.chain) + 1,
                'timestamp': time(),
                'transactions': self.current_transactions,
                'validator': validator,
                'previous_hash': previous_hash or self.hash(self.chain[-1]),
            }
            self.current_transactions = []
            self.chain.append(block)
            self.save_data()
            self.backup_to_cloud()
            logging.info(f"New block created: {block['index']}")
            return block
        except Exception as e:
            logging.error(f"Error creating new block: {e}")
            raise e

    def new_transaction(self, sender, recipient, amount, signature, public_key, metadata=None):
        try:
            if sender != "0":
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
            logging.info(f"New transaction added: {transaction}")
            return self.last_block['index'] + 1 if self.chain else 1
        except Exception as e:
            logging.error(f"Error adding transaction: {e}")
            raise e

    def analyze_transactions_with_ai(self):
        transactions = [
            [tx["amount"], tx.get("metadata", {}).get("risk_score", 0)]
            for block in self.chain for tx in block["transactions"]
        ]
        if not transactions:
            return []
        try:
            from sklearn.ensemble import IsolationForest
            model = IsolationForest(contamination=0.05)
            model.fit(transactions)
            anomalies = [
                block["transactions"][i]
                for block in self.chain
                for i, tx in enumerate(block["transactions"])
                if model.predict([[tx["amount"], tx.get("metadata", {}).get("risk_score", 0)]]) == -1
            ]
            logging.info(f"Anomalies detected: {anomalies}")
            return anomalies
        except Exception as e:
            logging.error(f"Error analyzing transactions: {e}")
            return []

    def deploy_smart_contract(self, contract_id, contract_code):
        self.smart_contracts[contract_id] = contract_code
        logging.info(f"Smart contract deployed: {contract_id}")
        return True

    def execute_contract(self, contract_id, method, args):
        if contract_id not in self.smart_contracts:
            raise ValueError("Contract not found")
        contract_code = self.smart_contracts[contract_id]
        try:
            exec(contract_code, globals())
            result = eval(f"{method}(**args)")
            logging.info(f"Executed contract {contract_id} method {method} with result: {result}")
            return result
        except Exception as e:
            logging.error(f"Error executing contract {contract_id}: {e}")
            raise e

    def save_data(self):
        try:
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
            logging.info("Blockchain data saved to database.")
        except Exception as e:
            logging.error(f"Error saving data to database: {e}")

    def load_data(self):
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT chain, current_transactions, tokens FROM blockchain")
            row = cursor.fetchone()
            if row:
                self.chain = json.loads(row[0])
                self.current_transactions = json.loads(row[1])
                tokens_data = json.loads(row[2])
                self.tokens = [Token.from_dict(token) for token in tokens_data] if isinstance(tokens_data, list) else []
                logging.info("Blockchain data loaded from database.")
            else:
                logging.info("No data found in database, starting fresh.")
        except Exception as e:
            logging.error(f"Error loading data from database: {e}")

    def backup_to_cloud(self):
        try:
            data = {
                "chain": self.chain,
                "current_transactions": self.current_transactions,
                "tokens": [token.to_dict() for token in self.tokens]
            }
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".json") as temp_file:
                json.dump(data, temp_file, indent=4)
                temp_file_path = temp_file.name
            response = cloudinary.uploader.upload(
                temp_file_path,
                resource_type="raw",
                folder=CLOUDINARY_FOLDER,
                public_id=f"blockchain_backup_{int(time())}"
            )
            logging.info(f"Blockchain backed up to cloud: {response.get('secure_url')}")
        except Exception as e:
            logging.error(f"Error backing up to cloud: {e}")

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1] if self.chain else None

    def get_pending_transactions(self):
        return self.current_transactions

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
