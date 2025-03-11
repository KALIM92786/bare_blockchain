from web3 import Web3

class EVM:
    def __init__(self, rpc_url="http://localhost:8545"):
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        if self.w3.is_connected():
            print("✅ EVM connected successfully!")
        else:
            raise ConnectionError("❌ EVM connection failed!")

    def execute(self, contract_address, abi, method, *args):
        contract = self.w3.eth.contract(address=contract_address, abi=abi)
        try:
            func = contract.functions[method](*args)
            txn = func.build_transaction({
                'from': self.w3.eth.accounts[0],
                'nonce': self.w3.eth.get_transaction_count(self.w3.eth.accounts[0]),
                'gas': 3000000,
                'gasPrice': self.w3.to_wei('50', 'gwei')
            })
            # Replace 'YOUR_PRIVATE_KEY' with your actual private key or integrate securely.
            signed_txn = self.w3.eth.account.sign_transaction(txn, private_key="YOUR_PRIVATE_KEY")
            txn_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            receipt = self.w3.eth.wait_for_transaction_receipt(txn_hash)
            return receipt
        except Exception as e:
            return {"error": str(e)}
