// src/components/Explorer.js
import React, { useEffect, useState } from 'react';
import { Container, Typography, Paper, List, ListItem, ListItemText, CircularProgress } from '@mui/material';

const Explorer = () => {
  const [blocks, setBlocks] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/chain')
      .then(res => res.json())
      .then(data => {
        setBlocks(data.chain || []);
        setLoading(false);
      })
      .catch(err => {
        console.error("Error fetching blockchain data:", err);
        setLoading(false);
      });
  }, []);

  return (
    <Container>
      <Typography variant="h4" gutterBottom>Blockchain Explorer</Typography>
      <Paper elevation={3} sx={{ padding: 2 }}>
        {loading ? (
          <CircularProgress />
        ) : (
          <List>
            {blocks.map((block) => (
              <ListItem key={block.index} divider>
                <ListItemText 
                  primary={`Block #${block.index} - Hash: ${block.hash || "N/A"}`} 
                  secondary={`Validator: ${block.validator || 'N/A'} | Previous Hash: ${block.previous_hash}`} 
                />
              </ListItem>
            ))}
          </List>
        )}
      </Paper>
    </Container>
  );
};

export default Explorer;
