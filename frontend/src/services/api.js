import axios from "axios";

const api = axios.create({
  baseURL: "https://banking-application-1-vl9z.onrender.com/accounts",
});

export default api;