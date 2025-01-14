import unittest
from unittest.mock import patch
from blockchain import Blockchain, Wallet


class TestBlockchain(unittest.TestCase):
    def setUp(self):
        self.blockchain = Blockchain()
        self.private_key, self.public_key = Wallet.generate_keys()

    def test_new_transaction(self):
        sender = "Alice"
        recipient = "Bob"
        amount = 10
        message = f"{sender}{amount}{recipient}"
        signature = Wallet.sign_transaction(self.private_key, message)

        index = self.blockchain.new_transaction(sender, recipient, amount, signature, self.public_key)
        self.assertEqual(index, self.blockchain.last_block['index'] + 1)

    def test_proof_of_work(self):
        proof = self.blockchain.proof_of_work(self.blockchain.last_block['proof'])
        self.assertTrue(self.blockchain.valid_proof(self.blockchain.last_block['proof'], proof))

    def test_resolve_conflicts(self):
        new_chain = [
            self.blockchain.chain[0],
            {
                'index': 2,
                'timestamp': 1234567890,
                'transactions': [{'sender': "Alice", 'recipient': "Bob", 'amount': 10}],
                'proof': self.blockchain.proof_of_work(self.blockchain.chain[0]['proof']),
                'previous_hash': Blockchain.hash(self.blockchain.chain[0])
            }
        ]

        with patch('requests.get') as mocked_get:
            mocked_get.return_value.status_code = 200
            mocked_get.return_value.json.return_value = {'length': len(new_chain), 'chain': new_chain}

            self.blockchain.register_node("http://node1.com")
            replaced = self.blockchain.resolve_conflicts()

            self.assertTrue(replaced)
            self.assertEqual(len(self.blockchain.chain), len(new_chain))


if __name__ == "__main__":
    unittest.main()
