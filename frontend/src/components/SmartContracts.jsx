import React, { useState } from "react";
import axios from "axios";

function SmartContracts() {
  const [form, setForm] = useState({
    contract_id: "",
    contract_code: "",
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = () => {
    axios
      .post("http://localhost:5000/smart-contract/deploy", form)
      .then((response) => {
        alert(response.data.message);
      })
      .catch((error) => {
        alert(error.response.data.error);
      });
  };

  return (
    <div className="mt-4">
      <h3>Deploy Smart Contract</h3>
      <input
        type="text"
        name="contract_id"
        placeholder="Contract ID"
        onChange={handleChange}
        className="form-control mb-2"
      />
      <textarea
        name="contract_code"
        placeholder="Contract Code"
        onChange={handleChange}
        className="form-control mb-2"
      ></textarea>
      <button onClick={handleSubmit} className="btn btn-info">
        Deploy Contract
      </button>
    </div>
  );
}

export default SmartContracts;
