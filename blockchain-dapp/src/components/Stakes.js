// src/components/Stakes.js
import React, { useEffect, useState } from 'react';
import { Container, Typography, Paper, List, ListItem, ListItemText } from '@mui/material';

const Stakes = () => {
  const [stakes, setStakes] = useState([]);

  useEffect(() => {
    fetch('/stakes')
      .then(res => res.json())
      .then(data => {
        // If data.stakes is an object, convert it to an array
        if (data.stakes && typeof data.stakes === 'object' && !Array.isArray(data.stakes)) {
          const stakesArray = Object.entries(data.stakes).map(([user, amount]) => ({ user, amount }));
          setStakes(stakesArray);
        } else if (Array.isArray(data.stakes)) {
          setStakes(data.stakes);
        } else {
          setStakes([]);
        }
      })
      .catch(err => console.error("Error fetching stakes:", err));
  }, []);

  return (
    <Container>
      <Typography variant="h4" gutterBottom>Current Stakes</Typography>
      <Paper elevation={3} sx={{ padding: 2 }}>
        <List>
          {stakes.map((stake, index) => (
            <ListItem key={index} divider>
              <ListItemText 
                primary={`User: ${stake.user}`} 
                secondary={`Amount: ${stake.amount} tokens`} 
              />
            </ListItem>
          ))}
        </List>
      </Paper>
    </Container>
  );
};

export default Stakes;
