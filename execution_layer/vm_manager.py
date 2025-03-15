from .evm_vm import EVM
from .wasm_vm import WASM
from .move_vm import MoveVM

class VMManager:
    def __init__(self):
        self.evm = EVM()       # EVM module: dynamic contract interaction enabled
        self.wasm = WASM()     # WASM module: warns if example.wasm is missing
        self.move_vm = MoveVM()  # MoveVM placeholder

    def execute_code(self, vm_type, *args):
        if vm_type == 'evm':
            return self.evm.execute(*args)
        elif vm_type == 'wasm':
            return self.wasm.execute(*args)
        elif vm_type == 'move':
            return self.move_vm.execute(*args)
        else:
            raise ValueError("❌ Invalid VM type specified.")
