import requests
import hashlib
import json
from time import time
from urllib.parse import urlparse
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
import logging
import base64
from cryptography.hazmat.primitives.serialization import load_pem_private_key

logging.basicConfig(level=logging.INFO)

SECRET_KEY = "your_shared_secret_key"  # Replace with a secure shared key

class Wallet:
    """
    Handles key pair generation and transaction signing.
    """

    @staticmethod
    def generate_keys():
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()

        # Serialize the keys
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
        self.smart_contracts = []  # Store contracts
        self.nodes = set()
        # Create the genesis block
        self.new_block(previous_hash='1', proof=100)

    def add_smart_contract(self, contract):
        """Adds a new smart contract to the blockchain."""
        self.smart_contracts.append(contract)
        print(f"Smart contract added: {contract.sender} -> {contract.receiver} for {contract.amount} tokens")

    def execute_contracts(self):
        """Executes all stored smart contracts."""
        for contract in self.smart_contracts:
            contract.execute()

    def register_node(self, address, secret_key):
        if secret_key != SECRET_KEY:
            raise ValueError("Unauthorized node registration. Secret key mismatch.")

        parsed_url = urlparse(address)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            self.nodes.add(parsed_url.path)          
        else:
            raise ValueError("Invalid URL")

    def new_transaction(self, sender, recipient, amount, signature, public_key):
        """
        Creates a new transaction.
        :param sender: The address of the sender.
        :param recipient: The address of the recipient.
        :param amount: The amount to transfer.
        :param signature: The digital signature to verify the sender's identity.
        :param public_key: The public key of the sender to verify the signature.
        :return: The index of the block that will hold this transaction.
        """
        # Verify the signature
        if not self.verify_signature(sender, signature, public_key):
            raise ValueError("Invalid signature")
        # Create a new transaction
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
            'timestamp': time()
        })
        return self.last_block['index'] + 1  # Return the index of the next block to hold this transaction

    def verify_signature(self, sender, signature, public_key):
        """
        Verifies a digital signature for a given message using the sender's public key. 
        :param sender: The address of the sender.
        :param signature: The digital signature.
        :param public_key: The public key of the sender.
        :return: True if the signature is valid, False otherwise.
        """
        message = f"{sender}{time()}"
        return Wallet.verify_signature(public_key, message, signature)

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
        return block

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

    def resolve_conflicts(self):
        """
        Consensus Algorithm:
        Resolves conflicts by replacing our chain with the longest one in the network.
        """
        neighbours = self.nodes  # Ensure nodes is a set of neighboring nodes
        new_chain = None
        max_length = len(self.chain)

        for node in neighbours:
            try:
                response = requests.get(f'http://{node}/chain')
                if response.status_code == 200:
                    length = response.json()['length']
                    chain = response.json()['chain']

                    # Check if the chain is longer and valid
                    if length > max_length and self.validate_chain(chain):
                        max_length = length
                        new_chain = chain
            except requests.exceptions.RequestException as e:
                logging.warning(f"Error connecting to node {node}: {e}")

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True

        return False

# Generate wallet keys (Example Usage)
private_key, public_key = Wallet.generate_keys()
logging.info("Private Key:\n" + private_key)
logging.info("Public Key:\n" + public_key)

