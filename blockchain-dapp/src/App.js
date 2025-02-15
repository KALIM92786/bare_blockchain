// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { AppBar, Toolbar, Typography, Container, Button } from '@mui/material';
import Explorer from './components/Explorer';
import Stakes from './components/Stakes';
import Transactions from './components/Transactions';
import StakingForm from './components/StakingForm'; // For staking tokens

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
        </Toolbar>
      </AppBar>
      <Container sx={{ marginTop: 4 }}>
        <Routes>
          <Route path="/" element={<Explorer />} />
          <Route path="/stakes" element={<Stakes />} />
          <Route path="/transactions" element={<Transactions />} />
          <Route path="/staking" element={<StakingForm />} />
        </Routes>
      </Container>
    </Router>
  );
}

export default App;
