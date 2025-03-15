import React, { useEffect, useState } from 'react';
import { Container, Typography, Paper, List, ListItem, ListItemText } from '@mui/material';

const Transactions = () => {
  const [transactions, setTransactions] = useState([]);

  useEffect(() => {
    fetch("http://localhost:5000/chain")
      .then(res => res.json())
      .then(data => {
        let allTx = [];
        data.chain.forEach(block => {
          if (block.transactions && block.transactions.length > 0) {
            block.transactions.forEach(tx => {
              allTx.push({ blockIndex: block.index, ...tx });
            });
          }
        });
        setTransactions(allTx);
      })
      .catch(err => console.error("Error fetching transactions:", err));
  }, []);

  return (
    <Container>
      <Typography variant="h4" gutterBottom>Recent Transactions</Typography>
      <Paper elevation={3} sx={{ padding: 2 }}>
        <List>
          {transactions.map((tx, index) => (
            <ListItem key={index} divider>
              <ListItemText 
                primary={`From: ${tx.sender} → To: ${tx.recipient}`} 
                secondary={`Amount: ${tx.amount} tokens | Block: ${tx.blockIndex}`} 
              />
            </ListItem>
          ))}
        </List>
      </Paper>
    </Container>
  );
};

export default Transactions;
