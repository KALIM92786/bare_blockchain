# Bare Blockchain

**Bare Blockchain** is a simple, functional blockchain implemented in Python using Flask. It provides basic blockchain functionality, including transaction management, mining, and consensus.

---

## **Features**
- Blockchain basics:
  - Adding transactions.
  - Mining blocks using Proof of Work (PoW).
  - Resolving conflicts via the longest chain rule.
- Cryptography:
  - RSA key pair generation for secure transactions.
  - Digital signature verification to ensure transaction authenticity.
- Flask API:
  - Endpoints to interact with the blockchain.
  - Add transactions, mine blocks, view the chain, and register nodes.
- Smart Contract Support:
  - Add and execute smart contracts with custom conditions.
- Secure API using JWT for authentication.

---

## **Installation**

### **Prerequisites**
- Python 3.8 or higher
- Flask and related dependencies
- Cryptography library
- A modern browser (for frontend testing)

### **Setup Instructions**
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/bare-blockchain.git
   cd bare-blockchain
