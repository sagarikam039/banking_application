import { useEffect, useState } from "react";
import api from "../services/api";
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";

function Dashboard() {
  const [account, setAccount] = useState(null);
  const [risk, setRisk] = useState(null);
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

          const handleLogout = () => {
            localStorage.removeItem("access_token");
            localStorage.removeItem("refresh_token");

            navigate("/login");
      };
  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const token = localStorage.getItem("access_token");

        const accountResponse = await api.get("/api/accounts/", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        const riskResponse = await api.get("/api/risk-analyzer/", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        setAccount(accountResponse.data);
        setRisk(riskResponse.data);

          

      } catch (error) {
        setMessage("Unable to load dashboard details");
      }
    };

    fetchDashboardData();
  }, []);

  return (
    <div className="hero">
      <h1>Dashboard</h1>

      {message && <p>{message}</p>}

      {account && (
        <div>
          <h2>Account Details</h2>

          <p><strong>Username:</strong> {account.username}</p>
          <p><strong>Account Number:</strong> {account.account_number}</p>
          <p><strong>Balance:</strong> ${account.balance}</p>
          <div className="dashboard-buttons">
            <Link to="/deposit">
              <button>Deposit</button>
            </Link>
            <Link to="/withdraw">
              <button>Withdraw</button>
            </Link>
            <Link to="/transfer">
              <button>Transfer</button>
            </Link>
            <Link to="/transactions">
              <button>Transactions</button> 
            </Link>
          </div>
         <div style={{ marginTop: "20px" }}>
            <button onClick={handleLogout} className="logout-btn">
              Logout
            </button>
          </div>
        </div>
      )}

      {risk && (
        <div className="risk-card">
          <h2>AI/ML Spending Risk Analyzer</h2>

          <p><strong>Risk Level:</strong> {risk.risk_level}</p>
          <p><strong>Reason:</strong> {risk.reason}</p>
          <p><strong>Total Transactions:</strong> {risk.total_transactions}</p>
          <p><strong>Withdrawals:</strong> {risk.total_withdrawals}</p>
          <p><strong>Transfers:</strong> {risk.total_transfers}</p>
        </div>
      )}
    </div>
  );


}

export default Dashboard;