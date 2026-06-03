import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import { Link } from "react-router-dom";
function Transfer() {
  const [senderAccount, setSenderAccount] = useState("");
  const [receiverAccount, setReceiverAccount] = useState("");
  const [amount, setAmount] = useState("");
  const [message, setMessage] = useState("");

  const navigate = useNavigate();

  const handleTransfer = async (e) => {
    e.preventDefault();

    try {
      const token = localStorage.getItem("access_token");

      const response = await api.post(
        "/api/transfer/",
        {
          sender_account: senderAccount,
          receiver_account: receiverAccount,
          amount: amount,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setMessage(response.data.message || "Transfer successful");

      setTimeout(() => {
        navigate("/dashboard");
      }, 1000);
    } catch (error) {
      console.log(error.response?.data);
      setMessage("Transfer failed. Please check account numbers and balance.");
    }
  };

  return (
    <div className="hero">
      <h1>Transfer Money</h1>

      {message && <p>{message}</p>}

      <form className="form-container" onSubmit={handleTransfer}>
        <input
          type="text"
          placeholder="Sender Account Number"
          value={senderAccount}
          onChange={(e) => setSenderAccount(e.target.value)}
          required
        />

        <input
          type="text"
          placeholder="Receiver Account Number"
          value={receiverAccount}
          onChange={(e) => setReceiverAccount(e.target.value)}
          required
        />

        <input
          type="number"
          placeholder="Enter Transfer Amount"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
          required
        />

        <button type="submit">Transfer</button>
        <div style={{ marginTop: "20px" }}>
          <Link to="/dashboard">
            <button>Back to Dashboard</button>
          </Link>
        </div>
      </form>
    </div>
  );
}

export default Transfer;