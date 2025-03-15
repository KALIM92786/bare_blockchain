import React, { useState } from 'react';
import { Box, TextField, Button, Typography, Paper, Alert, CircularProgress } from '@mui/material';

const Voting = () => {
  const [proposalId, setProposalId] = useState('');
  const [proposer, setProposer] = useState('');
  const [description, setDescription] = useState('');
  const [proposalType, setProposalType] = useState('');
  const [votingPeriod, setVotingPeriod] = useState('');
  const [vote, setVote] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  // Create a new governance proposal
  const createProposal = async () => {
    setLoading(true);
    try {
      const res = await fetch("http://localhost:5000/governance/proposal", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          proposal_id: proposalId,
          proposer,
          description,
          proposal_type: proposalType,
          voting_period: parseInt(votingPeriod, 10)
        })
      });
      const data = await res.json();
      setResult({ type: "proposal", data });
    } catch (err) {
      setResult({ type: "error", message: err.message });
    } finally {
      setLoading(false);
    }
  };

  // Cast vote on a proposal
  const castVote = async () => {
    setLoading(true);
    try {
      const res = await fetch("http://localhost:5000/governance/proposal/vote", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          proposal_id: proposalId,
          voter: proposer, // for demo purposes, using proposer address as voter
          vote: vote.toLowerCase() === "yes"
        })
      });
      const data = await res.json();
      setResult({ type: "vote", data });
    } catch (err) {
      setResult({ type: "error", message: err.message });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Paper sx={{ padding: 3, margin: 2 }}>
      <Typography variant="h5" gutterBottom>Governance Voting</Typography>
      
      <Box sx={{ my: 2 }}>
        <Typography variant="subtitle1">Create Proposal</Typography>
        <TextField
          label="Proposal ID"
          fullWidth
          value={proposalId}
          onChange={(e) => setProposalId(e.target.value)}
          margin="normal"
        />
        <TextField
          label="Proposer Address"
          fullWidth
          value={proposer}
          onChange={(e) => setProposer(e.target.value)}
          margin="normal"
        />
        <TextField
          label="Description"
          fullWidth
          multiline
          rows={3}
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          margin="normal"
        />
        <TextField
          label="Proposal Type"
          fullWidth
          value={proposalType}
          onChange={(e) => setProposalType(e.target.value)}
          margin="normal"
        />
        <TextField
          label="Voting Period (seconds)"
          fullWidth
          value={votingPeriod}
          onChange={(e) => setVotingPeriod(e.target.value)}
          margin="normal"
        />
        <Button variant="contained" onClick={createProposal} disabled={loading} fullWidth sx={{ mt: 2 }}>
          {loading ? <CircularProgress size={24} /> : "Create Proposal"}
        </Button>
      </Box>

      <Box sx={{ my: 2 }}>
        <Typography variant="subtitle1">Cast Vote</Typography>
        <TextField
          label="Vote (Yes/No)"
          fullWidth
          value={vote}
          onChange={(e) => setVote(e.target.value)}
          margin="normal"
        />
        <Button variant="contained" onClick={castVote} disabled={loading} fullWidth sx={{ mt: 2 }}>
          {loading ? <CircularProgress size={24} /> : "Cast Vote"}
        </Button>
      </Box>

      {result && result.type === "error" && (
        <Alert severity="error" sx={{ mt: 2 }}>
          {result.message}
        </Alert>
      )}
      {result && result.type !== "error" && (
        <Alert severity="success" sx={{ mt: 2 }}>
          <pre>{JSON.stringify(result.data, null, 2)}</pre>
        </Alert>
      )}
    </Paper>
  );
};

export default Voting;
