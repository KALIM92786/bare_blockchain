from .evm_vm import EVM
from .wasm_vm import WASM
from .move_vm import MoveVM

class VMManager:
    def __init__(self):
        # Instantiate each VM module
        self.evm = EVM()             # EVM module should connect to the local node
        self.wasm = WASM()           # WASM module will warn if example.wasm is not found
        self.move_vm = MoveVM()      # MoveVM placeholder

    def execute_code(self, vm_type, *args):
        if vm_type == 'evm':
            return self.evm.execute(*args)
        elif vm_type == 'wasm':
            return self.wasm.execute(*args)
        elif vm_type == 'move':
            return self.move_vm.execute(*args)
        else:
            raise ValueError("❌ Invalid VM type specified.")
