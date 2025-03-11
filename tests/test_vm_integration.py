import unittest
from execution_layer.vm_manager import VMManager

class TestVMIntegration(unittest.TestCase):
    def setUp(self):
        self.vm_manager = VMManager()

    def test_evm_execution(self):
        result = self.vm_manager.execute_code('evm', '0x5FbDB2315678afecb367f032d93F642f64180aa3', 
                                              [{'inputs': [], 'name': 'myMethod', 'outputs': []}], 
                                              'myMethod')
        self.assertIn('transactionHash', result)

    def test_wasm_execution(self):
        result = self.vm_manager.execute_code('wasm', 'sample_function', [5, 3])
        self.assertEqual(result, 8)

    def test_move_execution(self):
        result = self.vm_manager.execute_code('move', 'move_script', ['arg1', 'arg2'])
        self.assertIn('MoveVM executed successfully', result)

if __name__ == "__main__":
    unittest.main()

