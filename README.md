# 🚀 Bare Blockchain (PoS-Based)

## 📌 Project Overview

Bare Blockchain is a lightweight, decentralized blockchain application built with Python, Solidity, and React. It leverages a **Proof-of-Stake (PoS)** consensus mechanism—replacing energy-intensive Proof-of-Work (PoW)—for secure, efficient validation. The project provides an easy-to-understand platform for prototyping decentralized applications (DApps), token creation, staking, and smart contract execution.

## ✨ Features

### **Blockchain Core**
- ✅ **Decentralized Transaction Management**: Securely record and manage transactions on a persistent ledger.
- ✅ **Proof-of-Stake (PoS) Consensus**: Validators stake tokens instead of mining, making the blockchain energy-efficient and scalable.
- ✅ **Dynamic Validator Selection**: Randomly selects validators based on stake weight.
- ✅ **Conflict Resolution**: Implements a longest-chain rule to ensure network consensus.

### **Token & Staking System**
- ✅ **Custom Token Creation**: Define and issue your own tokens with unique symbols.
- ✅ **Token Transfers**: Securely transfer tokens between users.
- ✅ **Staking Mechanism**: Stake tokens to become a validator and earn rewards for validating new blocks.
- ✅ **Internal & Smart Contract Staking**: Supports both internal staking for consensus and smart contract-based staking for advanced use cases.

### **Smart Contract Integration**
- ✅ **Dynamic Contract Deployment**: Deploy custom smart contracts on demand.
- ✅ **Smart Contract Execution**: Execute deployed contracts with method calls and arguments.
- ✅ **Governance & Automation**: Use contracts to automate decentralized governance and digital agreements.

### **Security & Cryptography**
- ✅ **RSA Key Pair Generation**: Generate public/private key pairs for secure transactions.
- ✅ **Digital Signature Verification**: Ensure transaction authenticity with robust cryptographic validation.
- ✅ **Cloud Backups**: Periodically backup blockchain data to Cloudinary.

### **Developer & Learning Tools**
- ✅ **RESTful API**: Easy-to-use endpoints for interacting with the blockchain.
- ✅ **Extensible Architecture**: Modular design allows for adding new features like AI-based transaction analysis.
- ✅ **Local Development**: Includes a Hardhat environment for smart contract testing and debugging.
- ✅ **Deployment Automation**: Preconfigured deployment instructions for Render (backend) and Netlify/Vercel (frontend).

## 🛠️ Tech Stack

- **Smart Contracts**: Solidity, Hardhat
- **Backend**: Python, Flask, Web3.py
- **Frontend**: React.js
- **Database**: SQLite
- **Blockchain**: Ethereum (Alchemy & Hardhat)
- **Deployment**: Render (backend) & Netlify/Vercel (frontend)
- **Cloud Backup**: Cloudinary

## 📥 Installation & Setup

### 1️⃣ **Clone the Repository**

```sh
git clone https://github.com/KALIM92786/bare_blockchain.git
cd bare_blockchain
```

### 2️⃣ **Backend Setup**

```sh
cd backend
python -m venv venv
source venv/bin/activate  # For Linux/macOS
venv\Scripts\activate    # For Windows
pip install -r requirements.txt
```

### 3️⃣ **Smart Contracts Setup**

```sh
cd contracts
npm install
npx hardhat compile
```

### 4️⃣ **Frontend Setup**

```sh
cd frontend/blockchain-dapp
npm install
```

## 🚀 Running the Project

### **1️⃣ Start the Local Blockchain (Hardhat)**

```sh
cd contracts
npx hardhat node
```

### **2️⃣ Run the Backend (Flask API)**

```sh
cd backend
python app.py
```

### **3️⃣ Run the Frontend (React.js)**

```sh
cd frontend/blockchain-dapp
npm start
```

## 🌎 Deployment Instructions

### **🔹 Backend Deployment on Render**

1. Create an account at [**Render**](https://render.com/).
2. Connect your GitHub repo.
3. Use `render.yaml` for deployment automation.

### **🔹 Smart Contracts Deployment (Alchemy & Hardhat)**

1. Sign up at [**Alchemy**](https://www.alchemy.com/).
2. Create a project and get your **Alchemy API Key**.
3. Replace `YOUR_API_KEY` in your backend code (`app.py`):

```python
w3 = Web3(Web3.HTTPProvider('https://eth-mainnet.g.alchemy.com/v2/YOUR_API_KEY'))
```

4. Deploy your smart contracts to a test network (e.g., Goerli):

```sh
cd contracts
npx hardhat run scripts/deploy.js --network goerli
```

### **🔹 Frontend Deployment (Vercel / Netlify)**

- **For Vercel:** Run `vercel` in `frontend/blockchain-dapp`.
- **For Netlify:** Connect your repository on Netlify and set the build directory to `build` (generated via `npm run build`).

## 📡 API Endpoints

| Method | Endpoint        | Description |
|--------|---------------|-------------|
| GET    | `/chain`       | Retrieve the complete blockchain |
| POST   | `/transactions/new` | Add a new transaction to the blockchain |
| GET    | `/block/latest` | Get the latest block in the blockchain |
| GET    | `/transactions/pending` | Retrieve pending transactions |
| POST   | `/blockchain/stake_tokens` | Stake tokens to become a validator |
| GET    | `/balance/<address>` | Get token balance for a given address |
| GET    | `/staker/<address>` | Get staking details for a validator |
| POST   | `/stake` | Build a staking transaction |
| POST   | `/smart-contract/deploy` | Deploy a new smart contract |
| POST   | `/smart-contract/execute` | Execute a deployed smart contract method |
| POST   | `/nodes/register` | Register new nodes (requires API key) |
| GET    | `/nodes/resolve` | Resolve and update the blockchain with consensus |

## 💡 Benefits of Using Bare Blockchain

- 🌍 **Energy-Efficient Consensus**: Uses PoS instead of PoW, reducing energy consumption.
- 🔗 **Decentralized Validation**: Validators stake tokens to participate in block validation.
- 🔑 **Easy-to-Use API**: Provides a RESTful interface for blockchain operations.
- 🛠️ **Modular & Extensible**: Easily add new features like AI-based transaction analysis.
- 🎓 **Educational & Prototyping Tool**: Ideal for learning blockchain & smart contracts.
- 🚀 **Flexible Deployment**: Deploy via Render, Netlify, Vercel, or local environments.

## 🤝 Contributing

1. **Fork** the repository.
2. **Create a new branch** (e.g., `feature/your-feature`).
3. **Commit** your changes with clear messages.
4. **Push** your branch to GitHub and create a **Pull Request**.

## 🔒 License

This project is licensed under the MIT License. See the LICENSE file for details.

## 📧 Contact

- **Developer**: Kalim Ansari  
- **Email**: [KALIM199919@GMAIL.COM](mailto:KALIM199919@GMAIL.COM)

