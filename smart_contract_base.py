class SmartContract:
    def __init__(self, sender, receiver, amount, condition):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.condition = condition
        self.status = "pending"

    def execute(self):
        if self.condition():
            self.status = "executed"
            return True
        else:
            self.status = "failed"
            return False
