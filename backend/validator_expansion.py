import random

class Blockchain:
    def __init__(self):
        # Mapping of validator name to their stake amount
        self.validators = {}  
        # Total stake amount in the system
        self.total_stake = 0  
        # List of blocks (for demonstration purposes)
        self.blocks = []     

    def stake(self, validator, amount):
        """
        Allow a user to stake tokens. If the user already exists,
        increase their stake; otherwise, register them as a validator.
        """
        if validator in self.validators:
            self.validators[validator] += amount
        else:
            self.validators[validator] = amount
        self.total_stake += amount
        print(f"{validator} staked {amount} tokens. Total stake: {self.validators[validator]}")

    def slash(self, validator, penalty_percentage):
        """
        Slash (penalize) a validator by deducting a percentage of their stake.
        For example, a penalty_percentage of 0.2 removes 20% of the stake.
        """
        if validator not in self.validators:
            print(f"{validator} is not a validator.")
            return
        penalty_amount = self.validators[validator] * penalty_percentage
        self.validators[validator] -= penalty_amount
        self.total_stake -= penalty_amount
        print(f"{validator} has been slashed by {penalty_amount:.2f} tokens. New stake: {self.validators[validator]:.2f}")

    def select_validator(self):
        """
        Select a validator for block creation using weighted random selection,
        where a validator's chance is proportional to their stake.
        """
        if self.total_stake == 0:
            print("No stake in the system. Cannot select a validator.")
            return None
        
        r = random.uniform(0, self.total_stake)
        cumulative = 0
        for validator, stake in self.validators.items():
            cumulative += stake
            if r <= cumulative:
                return validator
        return None

    def reward_validator(self, validator, reward):
        """
        Reward the chosen validator for creating a block.
        Rewards are added to the validator's stake.
        """
        if validator in self.validators:
            self.validators[validator] += reward
            self.total_stake += reward
            print(f"{validator} rewarded with {reward} tokens. New stake: {self.validators[validator]}")
        else:
            print(f"{validator} is not a validator.")

    def create_block(self, data):
        """
        Create a new block. A validator is selected based on their stake,
        and then rewarded for block creation.
        """
        validator = self.select_validator()
        if validator is None:
            print("No validator selected. Block creation failed.")
            return None
        
        block = {
            "data": data,
            "validator": validator,
            "previous_hash": self.blocks[-1]["hash"] if self.blocks else "0",
            "hash": f"block_{len(self.blocks)+1}_hash"  # Dummy hash for demonstration
        }
        self.blocks.append(block)
        # Reward the validator (e.g., 10 tokens per block)
        self.reward_validator(validator, reward=10)
        print(f"Block created by {validator}: {block}")
        return block

# Demonstration of dynamic staking, slashing, and reward distribution
if __name__ == "__main__":
    # Create the blockchain instance
    bc = Blockchain()
    
    # Dynamic staking: Users can stake at any time
    bc.stake("Alice", 100)
    bc.stake("Bob", 50)
    bc.stake("Charlie", 75)
    
    # Create a block with current validators
    bc.create_block("Block data 1")
    
    # Simulate misbehavior and slash Bob by 20%
    bc.slash("Bob", 0.2)
    
    # Create another block after slashing
    bc.create_block("Block data 2")
