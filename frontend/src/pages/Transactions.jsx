import { useEffect, useState } from "react";
import api from "../services/api";
import { Link } from "react-router-dom";

function Transactions() {
  const [transactions, setTransactions] = useState([]);
  const [message, setMessage] = useState("");

  useEffect(() => {
    const fetchTransactions = async () => {
      try {
        const token = localStorage.getItem("access_token");

        const response = await api.get("/api/transactions/", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        setTransactions(response.data);
      } catch (error) {
        console.log(error.response?.data);
        setMessage("Unable to load transactions");
      }
    };

    fetchTransactions();
  }, []);

  return (
    <div className="hero">
      <h1>Transaction History</h1>

      {message && <p>{message}</p>}

      <table className="transaction-table">
        <thead>
          <tr>
            <th>Type</th>
            <th>Amount</th>
            <th>Date</th>
          </tr>
        </thead>

        <tbody>
          {transactions.map((transaction) => (
            <tr key={transaction.id}>
              <td>{transaction.transaction_type}</td>
              <td>${transaction.amount}</td>
              <td>{transaction.created_at}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <div style={{ marginTop: "20px" }}>
        <Link to="/dashboard">
          <button>Back to Dashboard</button>
        </Link>
      </div>
    </div>
  );
}

export default Transactions;