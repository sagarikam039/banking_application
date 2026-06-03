import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../services/api";

function Profile() {
  const [profile, setProfile] = useState(null);
  const [message, setMessage] = useState("");

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const token = localStorage.getItem("access_token");

        const response = await api.get("/api/profile/", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        setProfile(response.data);
      } catch (error) {
        console.log(error.response?.data);
        setMessage("Unable to load profile");
      }
    };

    fetchProfile();
  }, []);

  return (
    <div className="hero">
      <h1>My Profile</h1>

      {message && <p>{message}</p>}

      {profile && (
        <div>
          <p><strong>Username:</strong> {profile.username}</p>
          <p><strong>Email:</strong> {profile.email}</p>
          <p><strong>Account Number:</strong> {profile.account_number}</p>
          <p><strong>Balance:</strong> ${profile.balance}</p>
          <p><strong>Account Created:</strong> {profile.created_at}</p>
        </div>
      )}

      <div style={{ marginTop: "20px" }}>
        <Link to="/dashboard">
          <button>Back to Dashboard</button>
        </Link>
      </div>
    </div>
  );
}

export default Profile;