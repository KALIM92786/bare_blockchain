import requests
import hashlib
import json
from time import time
from urllib.parse import urlparse
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization

SECRET_KEY = "your_shared_secret_key"  # Replace with your secure shared key

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.nodes = set()
        # Create the genesis block
        self.new_block(previous_hash='1', proof=100)

    def register_node(self, address, secret_key):
        """
        Add a new node to the list of nodes.
        :param address: Address of the node.
        :param secret_key: Shared secret for authentication.
        """
        if secret_key != SECRET_KEY:
            raise ValueError("Unauthorized node registration.")

        parsed_url = urlparse(address)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError("Invalid URL")

    def resolve_conflicts(self):
        """
        Resolve conflicts by replacing our chain with the longest one in the network.
        :return: True if our chain was replaced, False otherwise.
        """
        neighbors = self.nodes
        new_chain = None

        max_length = len(self.chain)

        for node in neighbors:
            try:
                response = requests.get(f'https://{node}/chain', timeout=5)

                if response.status_code == 200:
                    length = response.json()['length']
                    chain = response.json()['chain']

                    if length > max_length and self.validate_chain(chain):
                        max_length = length
                        new_chain = chain
            except requests.exceptions.RequestException:
                print(f"Node {node} is unreachable.")

        if new_chain:
            self.chain = new_chain
            return True

        return False

    def new_block(self, proof, previous_hash=None):
        """
        Create a new block and add it to the chain.
        :param proof: Proof of Work.
        :param previous_hash: Hash of the previous block.
        :return: New block.
        """
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

    def new_transaction(self, sender, recipient, amount, signature, public_key):
        """
        Creates a new transaction to go into the next mined Block.
        :param sender: Address of the sender.
        :param recipient: Address of the recipient.
        :param amount: Amount to be transferred.
        :param signature: Digital signature of the transaction.
        :param public_key: Public key of the sender.
        :return: Index of the block that will hold this transaction.
        """
        if not sender or not recipient or amount <= 0:
            raise ValueError("Invalid transaction data.")

        transaction_data = f"{sender}{recipient}{amount}".encode()
        public_key_obj = serialization.load_pem_public_key(public_key.encode())
        try:
            public_key_obj.verify(
                signature.encode(),
                transaction_data,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
        except Exception:
            raise ValueError("Invalid transaction signature.")

        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
            'timestamp': time(),
            'id': hashlib.sha256(f"{sender}{recipient}{amount}{time()}".encode()).hexdigest(),
            'signature': signature,
            'public_key': public_key
        }
        self.current_transactions.append(transaction)
        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a block.
        :param block: Block dictionary.
        :return: Hash string.
        """
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        """
        Returns the last block in the chain.
        :return: Last block.
        """
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        """
        Simple Proof of Work Algorithm.
        :param last_proof: Previous proof.
        :return: Proof value.
        """
        proof = 0
        while not self.valid_proof(last_proof, proof):
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates the proof.
        :param last_proof: Previous proof.
        :param proof: Current proof.
        :return: True if valid, False otherwise.
        """
        guess = f"{last_proof}{proof}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def validate_chain(self, chain=None):
        """
        Validate the blockchain to ensure integrity.
        :param chain: Blockchain to validate. Defaults to the current chain.
        :return: True if valid, False otherwise.
        """
        chain = chain or self.chain
        for i in range(1, len(chain)):
            current_block = chain[i]
            previous_block = chain[i - 1]

            if current_block['previous_hash'] != self.hash(previous_block):
                return False

            if not self.valid_proof(previous_block['proof'], current_block['proof']):
                return False
        return True

    def find_transaction(self, transaction_id):
        """
        Find a transaction by its ID in the blockchain.
        :param transaction_id: ID of the transaction.
        :return: Transaction or None if not found.
        """
        for block in self.chain:
            for transaction in block['transactions']:
                if transaction['id'] == transaction_id:
                    return transaction
        return None
