import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../services/api";

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
      <h1>Welcome to MyBank {account?.username}</h1>

      {message && <p>{message}</p>}

      {account && risk && (
        <>
          <div className="dashboard-grid">
            <div className="dashboard-card">
              <h3>Account Number</h3>
              <p>{account.account_number}</p>
            </div>

            <div className="dashboard-card">
              <h3>Account Balance</h3>
              <p>${account.balance}</p>
            </div>

            <div className="dashboard-card">
              <h3>Risk Level</h3>
              <p>{risk.risk_level}</p>
            </div>
          </div>

          <div className="action-buttons">
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

            <Link to="/profile">
              <button>Profile</button>
            </Link>
          </div>

          <div style={{ marginTop: "20px" }}>
            <button onClick={handleLogout} className="logout-btn">
              Logout
            </button>
          </div>
        </>
      )}
    </div>
  );
}

export default Dashboard;