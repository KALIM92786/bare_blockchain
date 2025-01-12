import unittest
from unittest.mock import patch
from blockchain import Blockchain, Wallet
from smart_contract_base import SmartContract  # Ensure this is in a dedicated file

class TestSmartContract(unittest.TestCase):
    def setUp(self):
        """
        Set up a fresh blockchain and wallet for each test.
        """
        self.blockchain = Blockchain()
        self.wallet = Wallet()
        self.private_key, self.public_key = Wallet.generate_keys()

    def test_signature_verification(self):
        """
        Test that a digital signature is valid.
        """
        message = "fixed_message_for_testing"
        signature = self.wallet.sign_transaction(self.private_key, message)
        is_verified = self.wallet.verify_signature(self.public_key, message, signature)
        self.assertTrue(is_verified, "Signature should be valid")

    def test_add_and_execute_contract(self):
        """
        Test adding and executing a smart contract.
        """
        # Define a condition
        def always_true():
            return True

        # Create a contract
        contract = SmartContract(
            sender="Alice", 
            receiver="Bob", 
            amount=50, 
            condition=always_true
        )

        self.blockchain.add_smart_contract(contract)
        self.assertIn(contract, self.blockchain.smart_contracts, "Contract should be added to the blockchain")
        self.assertTrue(contract.execute(self.blockchain), "Contract should execute successfully")

    @patch('time.time', return_value=1234567890)
    def test_blockchain_transaction(self, mock_time):
        """
        Test adding a transaction and mining a block.
        """
        sender = "Alice"
        receiver = "Bob"
        amount = 10
        message = f"{sender}fixed_message_for_test"
        signature = self.wallet.sign_transaction(self.private_key, message)

        # Add transaction
        block_index = self.blockchain.new_transaction(sender, receiver, amount, signature, self.public_key)

        # Mine a block
        last_proof = self.blockchain.last_block['proof']
        proof = self.blockchain.proof_of_work(last_proof)
        self.blockchain.new_block(proof)

        # Validate transaction in the block
        last_block = self.blockchain.last_block
        self.assertEqual(last_block['index'], block_index, "Transaction should be added to the latest block")
        self.assertIn(
            {'sender': sender, 'recipient': receiver, 'amount': amount, 'timestamp': mock_time.return_value},
            last_block['transactions'],
            "Transaction should exist in the latest block"
        )

if __name__ == "__main__":
    unittest.main()
