import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import { Link } from "react-router-dom";
function Withdraw() {
  const [accountNumber, setAccountNumber] = useState("");
  const [amount, setAmount] = useState("");
  const [message, setMessage] = useState("");

  const navigate = useNavigate();

  const handleWithdraw = async (e) => {
    e.preventDefault();

    try {
      const token = localStorage.getItem("access_token");

      const response = await api.post(
        "/api/withdraw/",
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

      setMessage(response.data.message || "Amount withdrawn successfully");

      setTimeout(() => {
        navigate("/dashboard");
      }, 1000);

    } catch (error) {
      console.log(error.response?.data);
      setMessage("Withdraw failed. Please check account number, amount, or balance.");
    }
  };

  return (
    <div className="hero">
      <h1>Withdraw Money</h1>

      {message && <p>{message}</p>}

      <form className="form-container" onSubmit={handleWithdraw}>
        <input
          type="text"
          placeholder="Enter Account Number"
          value={accountNumber}
          onChange={(e) => setAccountNumber(e.target.value)}
          required
        />

        <input
          type="number"
          placeholder="Enter Withdraw Amount"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
          required
        />

        <button type="submit">Withdraw</button>

        <div style={{ marginTop: "20px" }}>
          <Link to="/dashboard">
            <button>Back to Dashboard</button>
          </Link>
        </div>
      </form>
    </div>
  );
}

export default Withdraw;