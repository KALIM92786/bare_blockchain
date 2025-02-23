from smart_contracts import SmartContract, ContractManager, simple_payment_contract

# Initialize the ContractManager
manager = ContractManager()

# Deploy the simple payment contract at a designated address, e.g., "contract1"
initial_state = {"Alice": 100}
payment_contract = SmartContract(simple_payment_contract, state=initial_state)
manager.deploy_contract("contract1", payment_contract)

# Simulate a transaction: Alice sends 30 tokens to Bob.
tx_data = {
    "from": "Alice",
    "to": "Bob",
    "amount": 30
}

# Call the contract and execute the transaction
result = manager.call_contract("contract1", None, tx_data)
print("Transaction result:", result)

# Check the updated state of the contract
print("Contract state:", payment_contract.state)
