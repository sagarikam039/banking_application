import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

function Deposit() {
  const [accountNumber, setAccountNumber] = useState("");
  const [amount, setAmount] = useState("");
  const [message, setMessage] = useState("");

  const navigate = useNavigate();

  const handleDeposit = async (e) => {
    e.preventDefault();

    try {
      const token = localStorage.getItem("access_token");

      await api.post(
        "/api/deposit/",
        {
          account_number: accountNumber,
          amount: amount,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setMessage("Amount deposited successfully");

      setTimeout(() => {
        navigate("/dashboard");
      }, 1000);

    } catch (error) {
      setMessage("Deposit failed. Please check account number and amount.");
    }
  };

  return (
    <div className="hero">
      <h1>Deposit Money</h1>

      {message && <p>{message}</p>}

      <form className="form-container" onSubmit={handleDeposit}>
        <input
          type="text"
          placeholder="Enter Account Number"
          value={accountNumber}
          onChange={(e) => setAccountNumber(e.target.value)}
          required
        />

        <input
          type="number"
          placeholder="Enter Deposit Amount"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
          required
        />

        <button type="submit">Deposit</button>
      </form>
    </div>
  );
}

export default Deposit;