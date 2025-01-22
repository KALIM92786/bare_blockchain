# Bare Blockchain

Bare Blockchain is a simple, functional blockchain implemented in Python using Flask. It provides basic blockchain functionality, including transaction management, mining, and consensus mechanisms. It also supports token creation, transfer, and smart contract execution.

---

## Features

### Blockchain Functionality:
- Add and manage transactions securely.
- Mine blocks using Proof of Work (PoW).
- Handle conflicts through the longest chain rule.

### Token Management:
- Create custom tokens with unique symbols.
- Transfer tokens between users with balance validation.

### Cryptography:
- RSA key pair generation for secure transactions.
- Digital signature verification to ensure transaction authenticity.

### Smart Contracts:
- Deploy and execute smart contracts with custom logic.
- Evaluate conditions dynamically for contract execution.

### Flask API:
- Endpoints to interact with the blockchain:
  - Add transactions.
  - Mine new blocks.
  - View the blockchain and transactions.
  - Register and resolve nodes.
  - Create and transfer tokens.
  - Deploy and execute smart contracts.

---

## Installation

### Prerequisites
- Python 3.8 or higher.
- Flask and related dependencies.
- Cryptography library (`cryptography` package).
- `gunicorn` for production deployment.

### Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/KALIM92786/bare-blockchain.git
   cd bare-blockchain


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
