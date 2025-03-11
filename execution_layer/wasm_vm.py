import os
import wasmtime

class WASM:
    def __init__(self, wasm_file="example.wasm"):
        # Check if the WASM file exists
        if not os.path.exists(wasm_file):
            print(f"Warning: {wasm_file} not found. WASM module will not be loaded.")
            self.module = None
            return
        try:
            # Initialize the Wasmtime engine and store
            self.engine = wasmtime.Engine()
            self.store = wasmtime.Store(self.engine)
            # Attempt to load the WASM module from file
            self.module = wasmtime.Module.from_file(self.engine, wasm_file)
            print("✅ WASM module loaded successfully with Wasmtime!")
        except Exception as e:
            raise Exception(f"Error loading WASM file with Wasmtime: {e}")

    def execute(self, function_name, *args):
        # If the module is not loaded, return an error
        if self.module is None:
            return {"error": "WASM module not loaded."}
        try:
            # Create a linker and instantiate the module
            linker = wasmtime.Linker(self.engine)
            instance = linker.instantiate(self.store, self.module)
            # Get the exported function by name
            func = instance.get_export(self.store, function_name)
            if func is None:
                return {"error": f"Function {function_name} not found in WASM module."}
            # Call the function with provided arguments
            result = func(self.store, *args)
            return result
        except Exception as e:
            return {"error": str(e)}
