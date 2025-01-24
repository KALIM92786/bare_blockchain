import React, { useState } from "react";
import axios from "axios";

function Transactions() {
  const [form, setForm] = useState({
    sender: "",
    recipient: "",
    amount: "",
    signature: "",
    public_key: "",
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = () => {
    axios
      .post("http://localhost:5000/transactions/new", form)
      .then((response) => {
        alert(response.data.message);
      })
      .catch((error) => {
        alert(error.response.data.error);
      });
  };

  return (
    <div className="mt-4">
      <h3>Create Transaction</h3>
      <input
        type="text"
        name="sender"
        placeholder="Sender"
        onChange={handleChange}
        className="form-control mb-2"
      />
      <input
        type="text"
        name="recipient"
        placeholder="Recipient"
        onChange={handleChange}
        className="form-control mb-2"
      />
      <input
        type="number"
        name="amount"
        placeholder="Amount"
        onChange={handleChange}
        className="form-control mb-2"
      />
      <input
        type="text"
        name="signature"
        placeholder="Signature"
        onChange={handleChange}
        className="form-control mb-2"
      />
      <input
        type="text"
        name="public_key"
        placeholder="Public Key"
        onChange={handleChange}
        className="form-control mb-2"
      />
      <button onClick={handleSubmit} className="btn btn-primary">
        Submit Transaction
      </button>
    </div>
  );
}

export default Transactions;
