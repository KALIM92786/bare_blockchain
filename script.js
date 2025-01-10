let token = null;

// Login to get the token
function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    fetch('http://127.0.0.1:5000/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    })
    .then(response => {
        if (response.status === 401) {
            alert('Invalid credentials!');
            return null;
        }
        return response.json();
    })
    .then(data => {
        if (data && data.token) {
            token = data.token;
            alert('Login successful!');
        }
    })
    .catch(error => console.error('Error:', error));
}

// Fetch the blockchain
function fetchBlockchain() {
    fetch('http://127.0.0.1:5000/chain', {
        method: 'GET',
        headers: {
            'x-access-token': token
        }
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('blockchain').innerHTML = JSON.stringify(data, null, 2);
    })
    .catch(error => console.error('Error:', error));
}

// Add a transaction
function createTransaction() {
    const sender = document.getElementById("sender").value;
    const recipient = document.getElementById("recipient").value;
    const amount = document.getElementById("amount").value;

    fetch('http://127.0.0.1:5000/transactions/new', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'x-access-token': token
        },
        body: JSON.stringify({ sender, recipient, amount })
    })
    .then(response => response.json())
    .then(data => alert(data.message))
    .catch(error => console.error('Error:', error));
}

// Mine a new block
function mineBlock() {
    fetch('http://127.0.0.1:5000/mine', {
        method: 'GET',
        headers: {
            'x-access-token': token
        }
    })
    .then(response => response.json())
    .then(data => alert(`New block mined: ${JSON.stringify(data, null, 2)}`))
    .catch(error => console.error('Error:', error));
}
