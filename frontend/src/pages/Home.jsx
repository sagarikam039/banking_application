import Navbar from "../components/Navbar";

function Home() {
  return (
    <div>
      <Navbar />

      <section className="hero">
        <h1>Modern Banking Application</h1>

        <p>
          Secure digital banking platform built with React and Django REST API.
        </p>

        <div className="hero-buttons">
          <button>Create Account</button>
          <button>Login</button>
        </div>
      </section>
    </div>
  );
}

export default Home;