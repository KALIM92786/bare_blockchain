from blockchain import Blockchain

# Initialize the blockchain
blockchain = Blockchain()

# Add a new transaction
blockchain.new_transaction(sender="Alice", recipient="Bob", amount=10)

# Mine a new block
last_proof = blockchain.last_block['proof']
proof = blockchain.proof_of_work(last_proof)
blockchain.new_block(proof)

# Validate the chain
is_valid = blockchain.validate_chain()
print(f"Blockchain valid: {is_valid}")

# Print the blockchain
for block in blockchain.chain:
    print(block)
