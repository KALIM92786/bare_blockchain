import React, { useEffect, useState } from "react";
import axios from "axios";

function Blockchain() {
  const [chain, setChain] = useState([]);

  useEffect(() => {
    axios.get("http://localhost:5000/chain").then((response) => {
      setChain(response.data.chain);
    });
  }, []);

  return (
    <div className="mt-4">
      <h3>Blockchain</h3>
      <ul className="list-group">
        {chain.map((block) => (
          <li key={block.index} className="list-group-item">
            <strong>Block #{block.index}</strong>
            <p>Proof: {block.proof}</p>
            <p>Previous Hash: {block.previous_hash}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Blockchain;
