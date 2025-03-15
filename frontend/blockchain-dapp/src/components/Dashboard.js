import React, { useEffect, useState } from "react";
import { Box, Typography, Paper, Grid, Button, CircularProgress } from "@mui/material";

const Dashboard = () => {
  const [chainData, setChainData] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchChainData = () => {
    setLoading(true);
    fetch("http://localhost:5000/chain")
      .then((res) => res.json())
      .then((data) => {
        setChainData(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching chain data:", err);
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchChainData();
  }, []);

  return (
    <Box sx={{ padding: "2rem" }}>
      <Grid container spacing={2}>
        <Grid item xs={12}>
          <Typography variant="h4" gutterBottom>
            Blockchain Dashboard
          </Typography>
          <Button variant="outlined" onClick={fetchChainData}>
            Refresh Data
          </Button>
        </Grid>
        <Grid item xs={12}>
          {loading ? (
            <CircularProgress />
          ) : chainData ? (
            <Paper sx={{ padding: "1rem" }}>
              <Typography variant="h6">Chain Length: {chainData.length}</Typography>
              <pre>{JSON.stringify(chainData.chain, null, 2)}</pre>
            </Paper>
          ) : (
            <Typography>No blockchain data available.</Typography>
          )}
        </Grid>
        <Grid item xs={12}>
          <Paper sx={{ padding: "1rem" }}>
            <Typography variant="h6">AI Analysis</Typography>
            <Typography variant="body1">
              AI analysis data will be displayed here once available.
            </Typography>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;
