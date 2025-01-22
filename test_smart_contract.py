import unittest
from smart_contract_base import SmartContract
from smart_contract import AdvancedSmartContract


class TestSmartContract(unittest.TestCase):
    def test_smart_contract_execution(self):
        """
        Test basic execution of the SmartContract.
        """
        def always_true():
            return True

        contract = SmartContract("Alice", "Bob", 50, always_true)
        self.assertEqual(contract.status, "pending")
        self.assertTrue(contract.execute())
        self.assertEqual(contract.status, "executed")

    def test_advanced_smart_contract(self):
        """
        Test execution and logging in AdvancedSmartContract.
        """
        def always_true():
            return True

        contract = AdvancedSmartContract("Alice", "Bob", 100, always_true)
        self.assertEqual(contract.status, "pending")
        self.assertTrue(contract.execute())
        log = contract.log_contract()
        self.assertEqual(log["sender"], "Alice")
        self.assertEqual(log["receiver"], "Bob")
        self.assertEqual(log["amount"], 100)
        self.assertEqual(log["status"], "executed")


if __name__ == "__main__":
    unittest.main()
