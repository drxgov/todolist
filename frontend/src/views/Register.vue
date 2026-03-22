<template>
    <div class="app">
        <div class="bg-orbs">
            <div class="orb orb-1"></div>
            <div class="orb orb-2"></div>
            <div class="orb orb-3"></div>
        </div>

        <div class="container">
            <div class="card">
                <div class="card-header">
                    <h1 class="logo">задачи</h1>
                    <p class="subtitle">создайте аккаунт</p>
                </div>

                <form @submit.prevent="handleRegister" class="form">
                    <div class="field">
                        <input
                            v-model="username"
                            type="text"
                            placeholder="Имя пользователя"
                            class="input"
                            required
                        />
                    </div>
                    <div class="field">
                        <input
                            v-model="password"
                            type="password"
                            placeholder="Пароль"
                            class="input"
                            required
                        />
                    </div>
                    <div class="field">
                        <input
                            v-model="passwordConfirm"
                            type="password"
                            placeholder="Повторите пароль"
                            class="input"
                            required
                        />
                    </div>

                    <p v-if="error" class="error">{{ error }}</p>
                    <p v-if="success" class="success-msg">{{ success }}</p>

                    <button type="submit" class="btn-submit">
                        Зарегистрироваться
                    </button>
                </form>

                <p class="footer-text">
                    Уже есть аккаунт?
                    <a href="/login" class="link">Войти</a>
                </p>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { register } from "../api/auth.js";

const username = ref("");
const password = ref("");
const passwordConfirm = ref("");
const error = ref("");
const success = ref("");
const router = useRouter();

const handleRegister = async () => {
    error.value = "";
    success.value = "";

    if (password.value !== passwordConfirm.value) {
        error.value = "Пароли не совпадают";
        return;
    }

    try {
        await register(username.value, password.value);
        success.value = "Аккаунт создан, перенаправляем...";
        setTimeout(() => router.push("/login"), 1500);
    } catch (e) {
        if (e.response?.status === 400) {
            error.value = "Пользователь с таким именем уже существует";
        } else {
            error.value = "Что-то пошло не так";
        }
    }
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Unbounded:wght@300;400;600&family=Onest:wght@300;400;500&display=swap");

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

.app {
    min-height: 100vh;
    background: #0a0a0f;
    font-family: "Onest", sans-serif;
    color: #e8e6f0;
    position: relative;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
}

.bg-orbs {
    position: fixed;
    inset: 0;
    pointer-events: none;
}

.orb {
    position: absolute;
    border-radius: 50%;
    filter: blur(80px);
    opacity: 0.35;
    animation: drift 12s ease-in-out infinite;
}

.orb-1 {
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, #7c3aed, transparent 70%);
    top: -100px;
    left: -100px;
    animation-delay: 0s;
}

.orb-2 {
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, #db2777, transparent 70%);
    top: 30%;
    right: -80px;
    animation-delay: -4s;
}

.orb-3 {
    width: 350px;
    height: 350px;
    background: radial-gradient(circle, #0ea5e9, transparent 70%);
    bottom: -50px;
    left: 30%;
    animation-delay: -8s;
}

@keyframes drift {
    0%,
    100% {
        transform: translate(0, 0) scale(1);
    }
    33% {
        transform: translate(30px, -20px) scale(1.05);
    }
    66% {
        transform: translate(-20px, 30px) scale(0.95);
    }
}

.container {
    position: relative;
    z-index: 1;
    width: 100%;
    max-width: 420px;
    padding: 24px;
}

.card {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 24px;
    padding: 40px 36px;
    backdrop-filter: blur(20px);
    animation: fadeUp 0.4s ease;
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
    background: linear-gradient(135deg, #c084fc, #f472b6, #60a5fa);
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
    background: rgba(255, 255, 255, 0.05);
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
    border-color: rgba(192, 132, 252, 0.4);
    background: rgba(255, 255, 255, 0.07);
    box-shadow: 0 0 0 3px rgba(192, 132, 252, 0.1);
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

.success-msg {
    font-size: 13px;
    color: #4ade80;
    text-align: center;
    padding: 8px 12px;
    background: rgba(74, 222, 128, 0.1);
    border: 1px solid rgba(74, 222, 128, 0.2);
    border-radius: 10px;
}

.btn-submit {
    width: 100%;
    padding: 14px;
    background: linear-gradient(135deg, #7c3aed, #db2777);
    border: none;
    border-radius: 14px;
    color: white;
    font-family: "Onest", sans-serif;
    font-size: 15px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
    margin-top: 4px;
    box-shadow: 0 4px 20px rgba(124, 58, 237, 0.4);
    letter-spacing: 0.3px;
}

.btn-submit:hover {
    box-shadow: 0 6px 28px rgba(124, 58, 237, 0.6);
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
    color: #c084fc;
    text-decoration: none;
    transition: color 0.2s;
}

.link:hover {
    color: #f472b6;
}
</style>
