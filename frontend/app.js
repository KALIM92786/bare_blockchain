// URL of your Flask API (replace this with the actual URL if needed)
const apiUrl = 'https://bare-blockchain.onrender.com';

// Show loading spinner
function showLoading() {
    document.getElementById('loading-spinner').style.display = 'block';
}

// Hide loading spinner
function hideLoading() {
    document.getElementById('loading-spinner').style.display = 'none';
}

// Example API call with loading spinner
function getBlockchain() {
    showLoading();
    fetch('https://bare-blockchain.onrender.com/chain')
        .then(response => response.json())
        .then(data => {
            console.log(data);
            hideLoading();
        })
        .catch(error => {
            showError('Failed to fetch the blockchain: ' + error.message);
            hideLoading();
        });
}


// Function to show success message
function showSuccess(message) {
    const successDiv = document.createElement('div');
    successDiv.classList.add('success');
    successDiv.innerHTML = `<strong>Success:</strong> ${message}`;
    document.body.appendChild(successDiv);
}

// Example API call to add a transaction
function addTransaction(sender, recipient, amount) {
    const transaction = { sender, recipient, amount };
    fetch('https://bare-blockchain.onrender.com/transactions/new', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(transaction)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showSuccess('Transaction added successfully');
        }
    })
    .catch(error => {
        showError('Failed to add transaction: ' + error.message);
    });
}



// Function to show error message
function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.classList.add('error');
    errorDiv.innerHTML = `<strong>Error:</strong> ${message}`;
    document.body.appendChild(errorDiv);
}

// Example API call with error handling
function getBlockchain() {
    fetch('https://bare-blockchain.onrender.com/chain')
        .then(response => response.json())
        .then(data => {
            console.log(data);
        })
        .catch(error => {
            showError('Failed to fetch the blockchain: ' + error.message);
        });
}




// Function to fetch and display the blockchain
async function loadBlockchain() {
    const response = await fetch(`${apiUrl}/chain`);
    const data = await response.json();
    const blockchainDiv = document.getElementById('blockchain');
    
    blockchainDiv.innerHTML = '<h2>Blockchain</h2>';
    data.chain.forEach((block, index) => {
        const blockElement = document.createElement('div');
        blockElement.classList.add('block');
        blockElement.innerHTML = `<strong>Block ${index + 1}:</strong><br>${JSON.stringify(block, null, 2)}`;
        blockchainDiv.appendChild(blockElement);
    });
}

// Function to handle transaction form submission
async function handleTransactionForm(event) {
    event.preventDefault();

    const sender = document.getElementById('sender').value;
    const receiver = document.getElementById('receiver').value;
    const amount = document.getElementById('amount').value;

    const response = await fetch(`${apiUrl}/transactions/new`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sender, receiver, amount })
    });

    if (response.ok) {
        alert('Transaction added successfully!');
    } else {
        alert('Failed to add transaction');
    }
}

// Function to handle mining block
async function mineBlock() {
    const miningStatus = document.getElementById('mining-status');
    miningStatus.textContent = 'Mining...';

    const response = await fetch(`${apiUrl}/mine`);
    const data = await response.json();

    if (data.success) {
        miningStatus.textContent = 'Block mined successfully!';
        loadBlockchain();
    } else {
        miningStatus.textContent = 'Mining failed.';
    }
}

// Event listeners
document.getElementById('load-chain').addEventListener('click', loadBlockchain);
document.getElementById('transaction-form').addEventListener('submit', handleTransactionForm);
document.getElementById('mine-block').addEventListener('click', mineBlock);
