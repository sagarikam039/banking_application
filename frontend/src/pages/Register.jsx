import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

function Register() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password1, setPassword1] = useState("");
  const [password2, setPassword2] = useState("");
  const [message, setMessage] = useState("");

  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();

    try {
      await api.post("/api/register/", {
        username,
        email,
        password1,
        password2,
      });

      setMessage("Account created successfully");

      setTimeout(() => {
        navigate("/login");
      }, 1000);
    } catch (error) {
      console.log(error.response?.data);
      setMessage("Registration failed. Please check details.");
    }
  };

  return (
    <div className="hero">
      <h1>Create Account</h1>

      {message && <p>{message}</p>}

      <form className="form-container" onSubmit={handleRegister}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <input
          type="password"
          placeholder="Password"
          value={password1}
          onChange={(e) => setPassword1(e.target.value)}
          required
        />

        <input
          type="password"
          placeholder="Confirm Password"
          value={password2}
          onChange={(e) => setPassword2(e.target.value)}
          required
        />

        <button type="submit">Register</button>
      </form>
    </div>
  );
}

export default Register;