// src/components/StakingForm.js
import React, { useState } from 'react';
import { Container, TextField, Button, Typography, Paper, CircularProgress, Alert } from '@mui/material';

const StakingForm = () => {
  const [user, setUser] = useState('');
  const [amount, setAmount] = useState('');
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const handleStake = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');
    try {
      const res = await fetch('/stake', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user, amount: parseInt(amount, 10) }),
      });
      const data = await res.json();
      setMessage(data.message || "Stake submitted!");
    } catch (error) {
      console.error("Error staking tokens:", error);
      setMessage("Error staking tokens.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container>
      <Typography variant="h4" gutterBottom>Stake Tokens</Typography>
      <Paper elevation={3} sx={{ padding: 3, maxWidth: 400, margin: 'auto' }}>
        <form onSubmit={handleStake}>
          <TextField
            label="User Address"
            fullWidth
            margin="normal"
            value={user}
            onChange={(e) => setUser(e.target.value)}
            required
          />
          <TextField
            label="Amount"
            type="number"
            fullWidth
            margin="normal"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            required
          />
          <Button variant="contained" color="primary" type="submit" fullWidth sx={{ mt: 2 }} disabled={loading}>
            {loading ? <CircularProgress size={24} /> : "Stake"}
          </Button>
        </form>
        {message && (
          <Alert severity="info" sx={{ mt: 2 }}>
            {message}
          </Alert>
        )}
      </Paper>
    </Container>
  );
};

export default StakingForm;
