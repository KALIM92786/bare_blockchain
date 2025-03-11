import unittest
from execution_layer.ai_module import AI_Module

class TestAIModule(unittest.TestCase):
    def setUp(self):
        self.ai = AI_Module()

    def test_low_amount(self):
        tx = {"amount": 500, "metadata": {}}
        analysis = self.ai.analyze_transaction(tx)
        self.assertEqual(analysis["risk_score"], 0.1)
        self.assertEqual(analysis["recommendation"], "Low risk: Transaction is acceptable.")

    def test_high_amount(self):
        tx = {"amount": 1500, "metadata": {}}
        analysis = self.ai.analyze_transaction(tx)
        self.assertEqual(analysis["risk_score"], 0.9)
        self.assertEqual(analysis["recommendation"], "High risk: Review transaction manually.")

if __name__ == "__main__":
    unittest.main()
