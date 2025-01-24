import React, { useState } from "react";
import axios from "axios";

function Tokens() {
  const [form, setForm] = useState({
    name: "",
    symbol: "",
    supply: "",
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = () => {
    axios
      .post("http://localhost:5000/tokens/create", form)
      .then((response) => {
        alert(response.data.message);
      })
      .catch((error) => {
        alert(error.response.data.error);
      });
  };

  return (
    <div className="mt-4">
      <h3>Create Token</h3>
      <input
        type="text"
        name="name"
        placeholder="Token Name"
        onChange={handleChange}
        className="form-control mb-2"
      />
      <input
        type="text"
        name="symbol"
        placeholder="Symbol"
        onChange={handleChange}
        className="form-control mb-2"
      />
      <input
        type="number"
        name="supply"
        placeholder="Supply"
        onChange={handleChange}
        className="form-control mb-2"
      />
      <button onClick={handleSubmit} className="btn btn-success">
        Create Token
      </button>
    </div>
  );
}

export default Tokens;
