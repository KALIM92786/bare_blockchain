# smart_contracts.py

class SmartContract:
    def __init__(self, contract_code, state=None):
        """
        contract_code: A function that defines the contract's logic.
        state: A dictionary to hold the contract's state.
        """
        self.contract_code = contract_code
        self.state = state if state is not None else {}

    def execute(self, blockchain, tx_data):
        """
        Execute the contract code with the provided blockchain context and transaction data.
        """
        return self.contract_code(blockchain, self.state, tx_data)


class ContractManager:
    def __init__(self):
        # A dictionary to store deployed contracts with their addresses.
        self.contracts = {}

    def deploy_contract(self, address, contract):
        """
        Deploy a new contract at a given address.
        """
        self.contracts[address] = contract
        print(f"Contract deployed at address: {address}")

    def call_contract(self, address, blockchain, tx_data):
        """
        Call (execute) the contract at the specified address.
        """
        if address not in self.contracts:
            print("Contract not found!")
            return None

        contract = self.contracts[address]
        result = contract.execute(blockchain, tx_data)
        return result

# This is an example of a simple payment contract function.
def simple_payment_contract(blockchain, state, tx_data):
    """
    tx_data should be a dictionary with keys:
      - 'from': sender's identifier
      - 'to': recipient's identifier
      - 'amount': amount to transfer
    
    The contract uses its internal state as a simple ledger for balances.
    """
    sender = tx_data.get("from")
    recipient = tx_data.get("to")
    amount = tx_data.get("amount")

    # Ensure the sender has enough balance in the contract's state.
    if state.get(sender, 0) >= amount:
        state[sender] -= amount
        state[recipient] = state.get(recipient, 0) + amount
        print(f"Contract executed: {amount} transferred from {sender} to {recipient}")
        return True
    else:
        print("Contract execution failed: insufficient funds!")
        return False
