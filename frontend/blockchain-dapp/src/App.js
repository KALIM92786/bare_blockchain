// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { AppBar, Toolbar, Typography, Container, Button } from '@mui/material';
import Explorer from './components/Explorer';
import Stakes from './components/Stakes';
import Transactions from './components/Transactions';
import StakingForm from './components/StakingForm';
import VmExecutor from "./components/VmExecutor";
import Dashboard from "./components/Dashboard";
import SmartContract from "./components/SmartContract";
import Voting from "./components/Voting"; // Governance/Voting component

function App() {
  return (
    <Router>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Blockchain DApp
          </Typography>
          <Button color="inherit" component={Link} to="/">Explorer</Button>
          <Button color="inherit" component={Link} to="/stakes">Stakes</Button>
          <Button color="inherit" component={Link} to="/transactions">Transactions</Button>
          <Button color="inherit" component={Link} to="/staking">Stake Tokens</Button>
          <Button color="inherit" component={Link} to="/vm">VM Executor</Button>
          <Button color="inherit" component={Link} to="/dashboard">Dashboard</Button>
          <Button color="inherit" component={Link} to="/smart-contract">Smart Contract</Button>
          <Button color="inherit" component={Link} to="/voting">Voting</Button>
        </Toolbar>
      </AppBar>
      <Container sx={{ marginTop: 4 }}>
        <Routes>
          <Route path="/" element={<Explorer />} />
          <Route path="/stakes" element={<Stakes />} />
          <Route path="/transactions" element={<Transactions />} />
          <Route path="/staking" element={<StakingForm />} />
          <Route path="/vm" element={<VmExecutor />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/smart-contract" element={<SmartContract />} />
          <Route path="/voting" element={<Voting />} />
        </Routes>
      </Container>
    </Router>
  );
}

export default App;
