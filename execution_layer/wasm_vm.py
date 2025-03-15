import os
import wasmtime

class WASM:
    def __init__(self, wasm_file="example.wasm"):
        if not os.path.exists(wasm_file):
            print(f"Warning: {wasm_file} not found. WASM module will not be loaded.")
            self.module = None
            return
        self.engine = wasmtime.Engine()
        self.store = wasmtime.Store(self.engine)
        try:
            self.module = wasmtime.Module.from_file(self.engine, wasm_file)
            print("✅ WASM module loaded successfully with Wasmtime!")
        except Exception as e:
            raise Exception(f"Error loading WASM file with Wasmtime: {e}")

    def execute(self, function_name, *args):
        if self.module is None:
            return {"error": "WASM module not loaded."}
        try:
            linker = wasmtime.Linker(self.engine)
            instance = linker.instantiate(self.store, self.module)
            func = instance.get_export(self.store, function_name)
            if func is None:
                return {"error": f"Function {function_name} not found in WASM module."}
            result = func(self.store, *args)
            return result
        except Exception as e:
            return {"error": str(e)}
