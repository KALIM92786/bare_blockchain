import React, { useState } from 'react';
import { Box, TextField, Button, Typography, Paper, Alert, CircularProgress } from '@mui/material';

const SmartContract = () => {
  const [contractId, setContractId] = useState("");
  const [contractCode, setContractCode] = useState("");
  const [deployMessage, setDeployMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const handleDeploy = async () => {
    setLoading(true);
    setDeployMessage("");
    try {
      const res = await fetch("http://localhost:5000/smart-contract/deploy", {
        method: "POST",
        headers: { 
          "Content-Type": "application/json",
          "x-api-key": "YOUR_API_KEY" // Replace with your actual API key or set via env variables
        },
        body: JSON.stringify({ contract_id: contractId, contract_code: contractCode }),
      });
      const data = await res.json();
      setDeployMessage(data.message || data.error);
    } catch (error) {
      console.error("Error deploying contract:", error);
      setDeployMessage("Error deploying contract.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Paper sx={{ padding: 3, margin: 2 }}>
      <Typography variant="h5" gutterBottom>Deploy Smart Contract</Typography>
      <TextField
        label="Contract ID"
        fullWidth
        value={contractId}
        onChange={(e) => setContractId(e.target.value)}
        margin="normal"
      />
      <TextField
        label="Contract Code"
        fullWidth
        multiline
        rows={6}
        value={contractCode}
        onChange={(e) => setContractCode(e.target.value)}
        margin="normal"
        placeholder="Enter your Solidity contract code or deployment script here."
      />
      <Box sx={{ position: "relative", mt: 2 }}>
        <Button variant="contained" onClick={handleDeploy} disabled={loading} fullWidth>
          {loading ? <CircularProgress size={24} /> : "Deploy Contract"}
        </Button>
      </Box>
      {deployMessage && (
        <Alert severity="info" sx={{ mt: 2 }}>
          {deployMessage}
        </Alert>
      )}
    </Paper>
  );
};

export default SmartContract;
