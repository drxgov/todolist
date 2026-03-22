import axios from "axios";

const api = axios.create({ baseURL: "/api" });

export const login = (username, password) => {
  return api.post("/auth/login", { username, password });
};

export const register = (username, password) => {
  return api.post("/auth/register", { username, password });
};
