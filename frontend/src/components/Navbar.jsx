import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav className="navbar">
      <h2>MyBank</h2>

      <div>
        <Link to="/login">
          <button>Login</button>
        </Link>

        <Link to="/register">
          <button>Create Account</button>
        </Link>
      </div>
    </nav>
  );
}

export default Navbar;