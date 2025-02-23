# 🚀 Bare Blockchain

## 📌 Project Overview
Bare Blockchain is a decentralized blockchain application that integrates smart contract staking and governance features. It leverages **Hardhat** for smart contract development, **Web3.py** for blockchain interaction, and **React** for a dynamic frontend. The project supports Alchemy for Ethereum blockchain connectivity.

## ✨ Features
- ✅ **Smart Contract Staking**
- ✅ **Governance Mechanism**
- ✅ **Ethereum Alchemy Integration**
- ✅ **Hardhat Local Blockchain**
- ✅ **Flask API Backend**
- ✅ **React.js Frontend**

## 🛠️ Tech Stack
- **Smart Contracts**: Solidity, Hardhat
- **Backend**: Python, Flask, Web3.py
- **Frontend**: React.js
- **Database**: SQLite
- **Blockchain**: Ethereum (Alchemy & Hardhat)

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

### **🔹 Backend (Render Deployment)**
1. Create an account at **[Render](https://render.com/)**.
2. Connect your GitHub repo.
3. Use `render.yaml` for deployment automation.

### **🔹 Smart Contracts (Alchemy & Hardhat)**
1. Sign up at **[Alchemy](https://www.alchemy.com/)**.
2. Create a project and get your **Alchemy API Key**.
3. Replace `YOUR_API_KEY` in `app.py`:
```python
w3 = Web3(Web3.HTTPProvider('https://eth-mainnet.g.alchemy.com/v2/YOUR_API_KEY'))
```
4. Deploy contracts:
```sh
cd contracts
npx hardhat run scripts/deploy.js --network goerli
```

### **🔹 Frontend (Vercel / Netlify)**
- **For Vercel:** Run `vercel` in `frontend/blockchain-dapp`.
- **For Netlify:** Connect repo and deploy.

## 📡 API Endpoints
| Method | Endpoint | Description |
|--------|---------|-------------|
| GET | `/api/balance` | Fetch user balance |
| POST | `/api/stake` | Stake tokens |
| POST | `/api/unstake` | Unstake tokens |
| GET | `/api/transactions` | Get transaction history |

## 🤝 Contributing
1. **Fork** the repo
2. **Create a new branch** (`feature-branch`)
3. **Commit** your changes
4. **Push** to GitHub & create a **PR**

## 🔒 License
This project is licensed under the MIT License. See the LICENSE file for details.

