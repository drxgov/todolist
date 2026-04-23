<template>
    <div class="app">
        <OrbBackground />

        <div class="container">
            <div class="card">
                <div class="card-header">
                    <h1 class="logo">задачи</h1>
                    <p class="subtitle">войдите в аккаунт</p>
                </div>

                <form @submit.prevent="handleLogin" class="form">
                    <div class="field">
                        <input
                            v-model="username"
                            type="text"
                            placeholder="Имя пользователя"
                            class="input"
                            autocomplete="username"
                            required
                        />
                    </div>
                    <div class="field">
                        <input
                            v-model="password"
                            type="password"
                            placeholder="Пароль"
                            class="input"
                            autocomplete="current-password"
                            required
                        />
                    </div>

                    <p v-if="error" class="error">{{ error }}</p>

                    <button type="submit" class="btn-submit">Войти</button>
                </form>

                <p class="footer-text">
                    Нет аккаунта?
                    <router-link to="/register" class="link"
                        >Зарегистрироваться</router-link
                    >
                </p>
            </div>
        </div>

        <SiteFooter />
    </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { login } from "../api/auth.js";
import { useAuth } from "../stores/auth.js";
import OrbBackground from "../components/OrbBackground.vue";
import SiteFooter from "../components/SiteFooter.vue";

const username = ref("");
const password = ref("");
const error = ref("");
const router = useRouter();
const { setToken } = useAuth();

const handleLogin = async () => {
    error.value = "";
    try {
        const response = await login(username.value, password.value);
        setToken(response.data.access_token);
        router.push("/tasks");
    } catch (e) {
        error.value = "Неверный логин или пароль";
    }
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Unbounded:wght@300;400;600&family=Onest:wght@300;400;500&display=swap");

.app {
    min-height: 100vh;
    background:
        radial-gradient(
            ellipse at top,
            rgba(45, 108, 255, 0.08) 0%,
            transparent 60%
        ),
        radial-gradient(
            ellipse at bottom,
            rgba(34, 227, 154, 0.06) 0%,
            transparent 60%
        ),
        #05070d;
    font-family: "Onest", sans-serif;
    color: #e8e6f0;
    position: relative;
    overflow: hidden;
    display: flex;
    flex-direction: column;
}

.container {
    position: relative;
    z-index: 1;
    flex: 1;
    width: 100%;
    max-width: 420px;
    margin: 0 auto;
    padding: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.card {
    width: 100%;
    background: linear-gradient(
        145deg,
        rgba(24, 32, 56, 0.55) 0%,
        rgba(12, 20, 34, 0.55) 100%
    );
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 24px;
    padding: 40px 36px;
    backdrop-filter: blur(20px);
    box-shadow: 0 30px 60px -20px rgba(0, 0, 0, 0.6);
    animation: fadeUp 0.4s ease;
    position: relative;
    overflow: hidden;
}

.card::before {
    content: "";
    position: absolute;
    inset: 0;
    padding: 1px;
    border-radius: 24px;
    background: linear-gradient(
        135deg,
        rgba(45, 108, 255, 0.6),
        rgba(34, 227, 154, 0.6)
    );
    -webkit-mask:
        linear-gradient(#000 0 0) content-box,
        linear-gradient(#000 0 0);
    -webkit-mask-composite: xor;
    mask-composite: exclude;
    opacity: 0.5;
    pointer-events: none;
}

@keyframes fadeUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.card-header {
    text-align: center;
    margin-bottom: 32px;
}

.logo {
    font-family: "Unbounded", sans-serif;
    font-size: 36px;
    font-weight: 600;
    background: linear-gradient(135deg, #2d6cff, #1ea7ff, #22e39a);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -1px;
    margin-bottom: 8px;
}

.subtitle {
    font-size: 13px;
    color: #6b6880;
    font-weight: 300;
    letter-spacing: 0.5px;
}

.form {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.field {
    width: 100%;
}

.input {
    width: 100%;
    background: rgba(5, 10, 20, 0.55);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 14px 18px;
    font-family: "Onest", sans-serif;
    font-size: 15px;
    color: #e8e6f0;
    outline: none;
    transition: all 0.2s;
}

.input::placeholder {
    color: #4a4760;
}

.input:focus {
    border-color: rgba(34, 227, 154, 0.5);
    background: rgba(5, 10, 20, 0.8);
    box-shadow: 0 0 0 3px rgba(34, 227, 154, 0.15);
}

.error {
    font-size: 13px;
    color: #f87171;
    text-align: center;
    padding: 8px 12px;
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid rgba(239, 68, 68, 0.2);
    border-radius: 10px;
}

.btn-submit {
    width: 100%;
    padding: 14px;
    background: linear-gradient(90deg, #2d6cff 0%, #22e39a 100%);
    background-size: 200% 100%;
    background-position: 0% 50%;
    border: none;
    border-radius: 14px;
    color: #051018;
    font-family: "Onest", sans-serif;
    font-size: 15px;
    font-weight: 600;
    cursor: pointer;
    transition:
        background-position 0.4s ease,
        box-shadow 0.2s ease,
        transform 0.05s ease;
    margin-top: 4px;
    box-shadow: 0 10px 30px -12px rgba(34, 227, 154, 0.5);
    letter-spacing: 0.3px;
}

.btn-submit:hover {
    background-position: 100% 50%;
    box-shadow: 0 14px 34px -12px rgba(34, 227, 154, 0.7);
    transform: translateY(-1px);
}

.btn-submit:active {
    transform: translateY(0);
}

.footer-text {
    text-align: center;
    font-size: 13px;
    color: #6b6880;
    margin-top: 24px;
}

.link {
    color: #22e39a;
    text-decoration: none;
    transition: color 0.2s;
}

.link:hover {
    color: #55f0b3;
}
</style>
