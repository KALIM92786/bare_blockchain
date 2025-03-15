// src/components/Governance.js
import React, { useState } from "react";
import { Box, TextField, Button, Typography, Paper, Alert, CircularProgress } from "@mui/material";

const Governance = () => {
  const [proposalId, setProposalId] = useState("");
  const [proposer, setProposer] = useState("");
  const [description, setDescription] = useState("");
  const [proposalType, setProposalType] = useState("");
  const [votingPeriod, setVotingPeriod] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const handleCreateProposal = async () => {
    setLoading(true);
    setMessage("");
    try {
      const res = await fetch("http://localhost:5000/governance/proposal", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          proposal_id: proposalId,
          proposer: proposer,
          description: description,
          proposal_type: proposalType,
          voting_period: Number(votingPeriod)
        }),
      });
      const data = await res.json();
      if (res.ok) {
        setMessage(data.proposal || data.message);
      } else {
        setMessage(data.error);
      }
    } catch (error) {
      setMessage("Error creating proposal: " + error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Paper sx={{ padding: 3, margin: 2 }}>
      <Typography variant="h5" gutterBottom>Create Governance Proposal</Typography>
      <TextField
        label="Proposal ID"
        fullWidth
        margin="normal"
        value={proposalId}
        onChange={(e) => setProposalId(e.target.value)}
      />
      <TextField
        label="Proposer Address"
        fullWidth
        margin="normal"
        value={proposer}
        onChange={(e) => setProposer(e.target.value)}
      />
      <TextField
        label="Description"
        fullWidth
        margin="normal"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
      />
      <TextField
        label="Proposal Type"
        fullWidth
        margin="normal"
        value={proposalType}
        onChange={(e) => setProposalType(e.target.value)}
      />
      <TextField
        label="Voting Period (seconds)"
        type="number"
        fullWidth
        margin="normal"
        value={votingPeriod}
        onChange={(e) => setVotingPeriod(e.target.value)}
      />
      <Box sx={{ position: "relative", marginTop: "1rem" }}>
        <Button variant="contained" onClick={handleCreateProposal} disabled={loading} fullWidth>
          {loading ? <CircularProgress size={24} /> : "Create Proposal"}
        </Button>
      </Box>
      {message && (
        <Alert severity="info" sx={{ marginTop: "1rem" }}>
          {message}
        </Alert>
      )}
    </Paper>
  );
};

export default Governance;
