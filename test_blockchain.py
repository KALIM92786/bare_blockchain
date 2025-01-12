import unittest
from blockchain import Blockchain, Wallet
from unittest.mock import patch

class TestBlockchain(unittest.TestCase):
    def setUp(self):
        """
        Set up a new blockchain and wallet for each test.
        """
        self.blockchain = Blockchain()
        self.wallet = Wallet()

        # Generate keys for transactions
        self.private_key, self.public_key = Wallet.generate_keys()

    def test_transaction_creation(self):
        """
        Test adding a transaction to the blockchain.
        """
        sender = "Alice"
        recipient = "Bob"
        amount = 10
        message = f"{sender} sends {amount} to {recipient}"
        signature = Wallet.sign_transaction(self.private_key, message)

        index = self.blockchain.new_transaction(sender, recipient, amount, signature, self.public_key)
        self.assertEqual(index, self.blockchain.last_block['index'] + 1, "Transaction should return the next block index")

    @patch('time.time', return_value=1234567890)
    def test_block_mining(self, mock_time):
        """
        Test mining a new block.
        """
        # Add a dummy transaction
        self.blockchain.new_transaction("Alice", "Bob", 10, "signature", "public_key")

        # Perform Proof of Work
        last_proof = self.blockchain.last_block['proof']
        proof = self.blockchain.proof_of_work(last_proof)

        # Create a new block
        block = self.blockchain.new_block(proof)
        self.assertEqual(block['proof'], proof, "Block proof should match the calculated proof")
        self.assertEqual(len(self.blockchain.chain), 2, "Blockchain should now have two blocks (genesis + mined)")

    def test_chain_structure(self):
        """
        Validate the blockchain structure.
        """
        self.assertGreaterEqual(len(self.blockchain.chain), 1, "Blockchain should always have at least the genesis block")
        genesis_block = self.blockchain.chain[0]
        self.assertEqual(genesis_block['index'], 1, "Genesis block should have an index of 1")
        self.assertEqual(genesis_block['previous_hash'], '1', "Genesis block should have a previous hash of '1'")

    def test_chain_validation(self):
        """
        Test the blockchain validation logic.
        """
        # Add a transaction and mine a block
        self.blockchain.new_transaction("Alice", "Bob", 10, "signature", "public_key")
        last_proof = self.blockchain.last_block['proof']
        proof = self.blockchain.proof_of_work(last_proof)
        self.blockchain.new_block(proof)

        # Simulate chain tampering
        self.blockchain.chain[1]['transactions'][0]['amount'] = 999

        # Implement validate_chain() and test it
        with self.assertRaises(Exception, msg="Tampered chain should raise an exception"):
            self.blockchain.validate_chain()

    def test_resolve_conflicts(self):
        """
        Test the conflict resolution logic.
        """
        # Mock nodes and their chains
        self.blockchain.register_node("http://node1.com", secret_key="your_shared_secret_key")
        self.blockchain.register_node("http://node2.com", secret_key="your_shared_secret_key")

        # Simulate a longer valid chain from a neighbor
        longer_chain = [
            self.blockchain.chain[0],  # Genesis block
            {
                'index': 2,
                'timestamp': 1234567890,
                'transactions': [{'sender': "Alice", 'recipient': "Bob", 'amount': 10}],
                'proof': 12345,
                'previous_hash': Blockchain.hash(self.blockchain.chain[0])
            }
        ]

        with patch('requests.get') as mocked_get:
            mocked_get.return_value.status_code = 200
            mocked_get.return_value.json.return_value = {'length': 2, 'chain': longer_chain}

            replaced = self.blockchain.resolve_conflicts()
            self.assertTrue(replaced, "Blockchain should replace its chain with the longer valid chain")
            self.assertEqual(len(self.blockchain.chain), 2, "Blockchain should now have two blocks")

if __name__ == '__main__':
    unittest.main()
