class SmartContract:
    def __init__(self, sender, receiver, amount, condition):
        """
        Initialize the smart contract with sender, receiver, amount, and condition.
        """
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.condition = condition
        self.status = "pending"

    def execute(self):
        """
        Execute the smart contract based on the condition.
        """
        if self.condition():
            self.status = "executed"
            return True
        else:
            self.status = "failed"
            return False
