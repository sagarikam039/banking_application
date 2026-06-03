import axios from "axios";

const API_BASE_URL = "https://banking-application-1-vl9z.onrender.com/accounts";

const api = axios.create({
  baseURL: API_BASE_URL,
});

export default api;