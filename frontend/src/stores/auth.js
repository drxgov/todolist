import { ref } from "vue";

const token = ref(localStorage.getItem("token"));

export const useAuth = () => {
  const setToken = (newToken) => {
    token.value = newToken;
    localStorage.setItem("token", newToken);
  };

  const logout = () => {
    token.value = null;
    localStorage.removeItem("token");
  };

  return { token, setToken, logout };
};
