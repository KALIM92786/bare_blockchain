import unittest
from blockchain import Blockchain
from smart_contract import SmartContract


class TestSmartContract(unittest.TestCase):
    def setUp(self):
        self.blockchain = Blockchain()

    def test_smart_contract_execution(self):
        def always_true():
            return True

        contract = SmartContract("Alice", "Bob", 50, always_true)
        self.blockchain.add_smart_contract(contract)
        self.assertIn(contract, self.blockchain.smart_contracts)
        self.assertTrue(contract.execute())
        self.assertEqual(contract.status, "executed")


if __name__ == "__main__":
    unittest.main()
