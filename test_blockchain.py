import unittest
from unittest.mock import patch
from blockchain import Blockchain, Wallet, Token


class TestBlockchain(unittest.TestCase):
    def setUp(self):
        """
        Set up a Blockchain instance and generate keys for tests.
        """
        self.blockchain = Blockchain()
        self.private_key, self.public_key = Wallet.generate_keys()

    def test_token_creation(self):
        """
        Test creating a new token and verifying its attributes.
        """
        token = Token("TestToken", "TTK", 1000)
        self.assertEqual(token.name, "TestToken")
        self.assertEqual(token.symbol, "TTK")
        self.assertEqual(token.total_supply, 1000)
        self.assertEqual(token.balances["admin"], 1000)

    def test_token_transfer(self):
        """
        Test transferring tokens between accounts.
        """
        token = Token("TestToken", "TTK", 1000)
        token.transfer("admin", "Alice", 200)
        self.assertEqual(token.balances["admin"], 800)
        self.assertEqual(token.balances["Alice"], 200)

    def test_new_transaction(self):
        """
        Test adding a new transaction to the blockchain.
        """
        sender = "Alice"
        recipient = "Bob"
        amount = 10
        message = f"{sender}{amount}{recipient}"
        signature = Wallet.sign_transaction(self.private_key, message)

        index = self.blockchain.new_transaction(sender, recipient, amount, signature, self.public_key)
        self.assertEqual(index, self.blockchain.last_block["index"] + 1)

    def test_proof_of_work(self):
        """
        Test the proof-of-work mechanism.
        """
        proof = self.blockchain.proof_of_work(self.blockchain.last_block["proof"])
        self.assertTrue(self.blockchain.valid_proof(self.blockchain.last_block["proof"], proof))

    def test_smart_contract_integration(self):
        """
        Test deploying and executing a smart contract in the blockchain.
        """
        contract_id = "contract_1"
        contract_code = """
def add(a, b):
    return a + b
"""
        self.blockchain.deploy_smart_contract(contract_id, contract_code)
        result = self.blockchain.execute_contract(contract_id, "add", {"a": 5, "b": 3})
        self.assertEqual(result, 8)

    def test_analyze_transactions(self):
        """
        Test identifying suspicious transactions.
        """
        sender = "Alice"
        recipient = "Bob"
        amount = 15000
        message = f"{sender}{amount}{recipient}"
        signature = Wallet.sign_transaction(self.private_key, message)

        self.blockchain.new_transaction(sender, recipient, amount, signature, self.public_key)
        suspicious = self.blockchain.analyze_transactions()
        self.assertEqual(len(suspicious), 1)
        self.assertEqual(suspicious[0]["amount"], 15000)


if __name__ == "__main__":
    unittest.main()
