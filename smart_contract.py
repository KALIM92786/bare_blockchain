from time import time
from smart_contract_base import SmartContract


class AdvancedSmartContract(SmartContract):
    def __init__(self, sender, receiver, amount, condition):
        """
        Inherits from SmartContract, adds advanced functionality.
        """
        super().__init__(sender, receiver, amount, condition)
        self.timestamp = time()

    def log_contract(self):
        """
        Logs the contract details for auditing purposes.
        """
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "status": self.status,
            "timestamp": self.timestamp
        }
