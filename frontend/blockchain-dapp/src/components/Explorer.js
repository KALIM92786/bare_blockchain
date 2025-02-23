// src/components/Explorer.js
import React, { useEffect, useState } from 'react';
import { Container, Typography, Paper, List, ListItem, ListItemText } from '@mui/material';

const Explorer = () => {
  const [blocks, setBlocks] = useState([]);

  useEffect(() => {
    // Fetch blockchain data from your backend (adjust URL if needed)
    fetch('/chain')
      .then(res => res.json())
      .then(data => setBlocks(data.chain || []))
      .catch(err => console.error("Error fetching blockchain data:", err));
  }, []);

  return (
    <Container>
      <Typography variant="h4" gutterBottom>Blockchain Explorer</Typography>
      <Paper elevation={3} sx={{ padding: 2 }}>
        <List>
          {blocks.map((block) => (
            <ListItem key={block.index} divider>
              <ListItemText 
                primary={`Block #${block.index} - Hash: ${block.hash}`} 
                secondary={`Validator: ${block.validator || 'N/A'} | Previous Hash: ${block.previous_hash}`} 
              />
            </ListItem>
          ))}
        </List>
      </Paper>
    </Container>
  );
};

export default Explorer;
