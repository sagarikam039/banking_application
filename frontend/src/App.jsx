import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import ProtectedRoute from "./components/ProtectedRoute";   

import Home from "./pages/Home";
import Register from "./pages/Register";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Deposit from "./pages/Deposit";
import Withdraw from "./pages/withdraw";
import Transfer from "./pages/Transfer";
import Transactions from "./pages/Transactions";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
            <Dashboard />
            </ProtectedRoute>
        }
        />
        <Route 
        path="/deposit" 
        element={
        <ProtectedRoute>
        <Deposit />
        </ProtectedRoute>} />
        <Route 
        path="/withdraw" 
        element={
        <ProtectedRoute>
        <Withdraw />
        </ProtectedRoute>} />
        <Route 
        path="/Transfer" 
        element={
        <ProtectedRoute>
        <Transfer />
        </ProtectedRoute>} />
        <Route 
        path="/transactions" 
        element={
        <ProtectedRoute>
        <Transactions />
        </ProtectedRoute>} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;