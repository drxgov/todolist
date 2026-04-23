<script setup>
const year = new Date().getFullYear();
</script>

<template>
    <footer class="site-footer">
        <span>© {{ year }} задачи. все права защищены.</span>
    </footer>
</template>

<style scoped>
.site-footer {
    position: relative;
    z-index: 2;
    padding: 18px 16px;
    text-align: center;
    font-family: "Onest", sans-serif;
    font-size: 12px;
    letter-spacing: 0.5px;
    color: #6b6880;
    border-top: 1px solid rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(6px);
    background: rgba(10, 10, 15, 0.35);
}
</style>
