import unittest
from execution_layer.vm_manager import VMManager

class TestVMIntegration(unittest.TestCase):
    def setUp(self):
        self.vm_manager = VMManager()

    def test_evm_execution(self):
        code = "evm_bytecode_example"
        result = self.vm_manager.execute_code(code, 'evm')
        self.assertEqual(result, "EVM Execution Successful")

if __name__ == '__main__':
    unittest.main()
