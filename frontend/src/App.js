import React from "react";
import Blockchain from "./components/Blockchain";
import Transactions from "./components/Transactions";
import Tokens from "./components/Tokens";
import SmartContracts from "./components/SmartContracts";

function App() {
  return (
    <div className="container mt-4">
      <h1 className="text-center">NextGen Blockchain System</h1>
      <Blockchain />
      <Transactions />
      <Tokens />
      <SmartContracts />
    </div>
  );
}

export default App;
