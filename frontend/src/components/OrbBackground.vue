<template>
    <div class="bg-orbs" aria-hidden="true">
        <div class="orb orb-1"></div>
        <div class="orb orb-2"></div>
        <div class="orb orb-3"></div>
    </div>
</template>

<style scoped>
.bg-orbs {
    position: fixed;
    inset: 0;
    pointer-events: none;
    overflow: hidden;
    z-index: 0;
}

.orb {
    position: absolute;
    top: 50%;
    left: 50%;
    width: 520px;
    height: 520px;
    border-radius: 50%;
    filter: blur(90px);
    opacity: 0.55;
    mix-blend-mode: screen;
    will-change: transform;
}

.orb-1 {
    background: radial-gradient(
        circle at 30% 30%,
        #2d6cff 0%,
        rgba(45, 108, 255, 0) 70%
    );
    animation: orbit-1 18s linear infinite;
}

.orb-2 {
    background: radial-gradient(
        circle at 30% 30%,
        #22e39a 0%,
        rgba(34, 227, 154, 0) 70%
    );
    animation: orbit-2 22s linear infinite;
}

.orb-3 {
    background: radial-gradient(
        circle at 30% 30%,
        #1ea7ff 0%,
        rgba(30, 167, 255, 0) 70%
    );
    animation: orbit-3 26s linear infinite;
}

@keyframes orbit-1 {
    from {
        transform: translate(-50%, -50%) rotate(0deg) translateX(260px)
            rotate(0deg);
    }
    to {
        transform: translate(-50%, -50%) rotate(360deg) translateX(260px)
            rotate(-360deg);
    }
}

@keyframes orbit-2 {
    from {
        transform: translate(-50%, -50%) rotate(120deg) translateX(300px)
            rotate(-120deg);
    }
    to {
        transform: translate(-50%, -50%) rotate(480deg) translateX(300px)
            rotate(-480deg);
    }
}

@keyframes orbit-3 {
    from {
        transform: translate(-50%, -50%) rotate(240deg) translateX(240px)
            rotate(-240deg);
    }
    to {
        transform: translate(-50%, -50%) rotate(600deg) translateX(240px)
            rotate(-600deg);
    }
}

@media (prefers-reduced-motion: reduce) {
    .orb {
        animation: none;
    }
}
</style>
