import unittest
from time import time
from blockchain import Blockchain, Wallet
from smart_contract import SmartContract
from smart_contract_base import SmartContract


class TestBlockchain(unittest.TestCase):
    
    def setUp(self):
        self.blockchain = Blockchain()
        self.wallet = Wallet()
        
        # Generate wallet keys
        self.private_key, self.public_key = Wallet.generate_keys()

    def test_signature_verification(self):
        # Create a transaction message
        message = "sender123" + "fixed_message_for_test"  # Fixed message to avoid timing issues
        signature = self.wallet.sign_transaction(self.private_key, message)
        
        # Verify the signature
        is_verified = self.wallet.verify_signature(self.public_key, message, signature)
        self.assertTrue(is_verified, "Signature should be valid")

    def test_add_and_execute_contract(self):
        # Define a condition function
        def contract_condition():
            return True  # Simulate a successful condition
        
        # Create a new smart contract
        contract = SmartContract(sender="sender123", receiver="receiver456", amount=50, condition=contract_condition)
        
        # Add it to the blockchain
        self.blockchain.add_smart_contract(contract)
        
        # Check if the contract exists in the blockchain's smart_contracts list
        self.assertIn(contract, self.blockchain.smart_contracts, "Contract should be added to the blockchain")
        
        # Execute the contract
        contract_executed = contract.execute()
        self.assertTrue(contract_executed, "Contract should be executed successfully")
        self.assertEqual(contract.status, "executed", "Contract status should be 'executed'")

    def test_blockchain_transaction(self):
        # Create a transaction
        sender = "sender123"
        receiver = "receiver456"
        amount = 50
        message = f"{sender}fixed_message_for_test"  # Fixed message to ensure consistency
        signature = self.wallet.sign_transaction(self.private_key, message)
        
        # Add a new transaction to the blockchain
        block_index = self.blockchain.new_transaction(sender, receiver, amount, signature, self.public_key)
        
        # Mine a new block
        self.blockchain.new_block(proof=12345)
        
        # Check if the transaction was successfully added to the block
        last_block = self.blockchain.last_block
        self.assertEqual(last_block['index'], block_index, "Transaction should be added to the latest block")
        self.assertIn(
            {'sender': sender, 'recipient': receiver, 'amount': amount, 'timestamp': last_block['timestamp']},
            last_block['transactions'],
            "Transaction should exist in the latest block"
        )

if __name__ == '__main__':
    unittest.main()
