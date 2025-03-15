# consensus/pos.py

import random
import logging

class ProofOfStake:
    def __init__(self):
        # A dictionary mapping validators (addresses) to their stake amounts
        self.stakes = {}

    def add_stake(self, validator, amount):
        """Add stake for a validator."""
        self.stakes[validator] = self.stakes.get(validator, 0) + amount
        logging.info(f"Validator {validator} now has stake: {self.stakes[validator]}")

    def remove_stake(self, validator, amount):
        """Remove stake from a validator."""
        if validator not in self.stakes or self.stakes[validator] < amount:
            raise ValueError("Insufficient stake")
        self.stakes[validator] -= amount
        logging.info(f"Validator {validator} now has stake: {self.stakes[validator]}")

    def select_validator(self):
        """Select a validator based on stake weights."""
        if not self.stakes:
            raise ValueError("No validators available")
        total_stake = sum(self.stakes.values())
        pick = random.uniform(0, total_stake)
        current = 0
        for validator, stake in self.stakes.items():
            current += stake
            if current >= pick:
                logging.info(f"Validator selected: {validator}")
                return validator
        return None

    def get_stake(self, validator):
        """Return the current stake for a given validator."""
        return self.stakes.get(validator, 0)
