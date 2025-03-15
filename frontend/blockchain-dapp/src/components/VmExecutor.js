import React, { useState } from "react";
import {
  Box,
  Button,
  TextField,
  Typography,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  CircularProgress,
  Alert,
  Snackbar
} from "@mui/material";

const VmExecutor = () => {
  const [vmType, setVmType] = useState("evm");
  const [params, setParams] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [snackbarOpen, setSnackbarOpen] = useState(false);

  const handleExecute = async () => {
    setError(null);
    setResult(null);
    let parsedParams;
    try {
      parsedParams = JSON.parse(params);
    } catch (err) {
      setError("Invalid JSON format in parameters.");
      setSnackbarOpen(true);
      return;
    }

    setLoading(true);
    try {
      const response = await fetch("http://localhost:5000/vm/execute", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          vm_type: vmType,
          params: parsedParams
        })
      });
      const data = await response.json();
      if (response.ok) {
        setResult(data.result);
      } else {
        setError(data.error);
      }
    } catch (err) {
      setError("Error executing VM endpoint: " + err.message);
    } finally {
      setLoading(false);
      setSnackbarOpen(true);
    }
  };

  return (
    <Box sx={{ padding: "1rem", border: "1px solid #ccc", margin: "1rem", borderRadius: "8px" }}>
      <Typography variant="h5" gutterBottom>
        VM Executor
      </Typography>
      
      <FormControl fullWidth margin="normal">
        <InputLabel id="vm-type-label">VM Type</InputLabel>
        <Select
          labelId="vm-type-label"
          value={vmType}
          label="VM Type"
          onChange={(e) => setVmType(e.target.value)}
        >
          <MenuItem value="evm">EVM</MenuItem>
          <MenuItem value="wasm">WASM</MenuItem>
          <MenuItem value="move">Move</MenuItem>
        </Select>
      </FormControl>
      
      <TextField
        label="Parameters (JSON Array)"
        multiline
        rows={4}
        fullWidth
        margin="normal"
        variant="outlined"
        value={params}
        onChange={(e) => setParams(e.target.value)}
        placeholder='e.g., ["0x...", [{"inputs": ...}], "balanceOf", "0x..."]'
      />
      
      <Box sx={{ position: "relative", marginTop: "1rem" }}>
        <Button variant="contained" onClick={handleExecute} disabled={loading} fullWidth>
          Execute
        </Button>
        {loading && (
          <CircularProgress
            size={24}
            sx={{
              position: "absolute",
              top: "50%",
              left: "50%",
              marginTop: "-12px",
              marginLeft: "-12px",
            }}
          />
        )}
      </Box>
      
      {result && (
        <Alert severity="success" sx={{ marginTop: "1rem" }}>
          <Typography variant="subtitle1">Result:</Typography>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </Alert>
      )}
      
      {error && (
        <Alert severity="error" sx={{ marginTop: "1rem" }}>
          <Typography variant="subtitle1">Error:</Typography>
          <pre>{error}</pre>
        </Alert>
      )}
      
      <Snackbar
        open={snackbarOpen}
        autoHideDuration={4000}
        onClose={() => setSnackbarOpen(false)}
        message={error ? "Error occurred" : "Execution successful"}
      />
    </Box>
  );
};

export default VmExecutor;

