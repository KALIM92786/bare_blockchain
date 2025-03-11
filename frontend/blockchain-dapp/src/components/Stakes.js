// src/components/Stakes.js
import React, { useEffect, useState } from 'react';
import { Container, Typography, Paper, List, ListItem, ListItemText, CircularProgress } from '@mui/material';

const Stakes = () => {
  const [stakes, setStakes] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/stakes')
      .then(res => res.json())
      .then(data => {
        let stakesArray = [];
        if (data.stakes && typeof data.stakes === 'object' && !Array.isArray(data.stakes)) {
          stakesArray = Object.entries(data.stakes).map(([user, amount]) => ({ user, amount }));
        } else if (Array.isArray(data.stakes)) {
          stakesArray = data.stakes;
        }
        setStakes(stakesArray);
        setLoading(false);
      })
      .catch(err => {
        console.error("Error fetching stakes:", err);
        setLoading(false);
      });
  }, []);

  return (
    <Container>
      <Typography variant="h4" gutterBottom>Current Stakes</Typography>
      <Paper elevation={3} sx={{ padding: 2 }}>
        {loading ? (
          <CircularProgress />
        ) : (
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
        )}
      </Paper>
    </Container>
  );
};

export default Stakes;
