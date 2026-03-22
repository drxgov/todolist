<template>
    <div class="app">
        <div class="bg-orbs">
            <div class="orb orb-1"></div>
            <div class="orb orb-2"></div>
            <div class="orb orb-3"></div>
        </div>

        <div class="container">
            <header class="header">
                <div class="header-left">
                    <h1 class="logo">задачи</h1>
                    <span class="task-count">{{ tasks.length }} задач</span>
                </div>
                <button @click="handleLogout" class="btn-logout">
                    <span>выйти</span>
                    <svg
                        width="16"
                        height="16"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                    >
                        <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
                        <polyline points="16 17 21 12 16 7" />
                        <line x1="21" y1="12" x2="9" y2="12" />
                    </svg>
                </button>
            </header>

            <form @submit.prevent="handleCreate" class="create-form">
                <div class="input-group">
                    <input
                        v-model="newTitle"
                        type="text"
                        placeholder="Что нужно сделать?"
                        class="input-main"
                        required
                    />
                    <input
                        v-model="newDescription"
                        type="text"
                        placeholder="Описание..."
                        class="input-desc"
                    />
                </div>
                <button type="submit" class="btn-add">
                    <svg
                        width="20"
                        height="20"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2.5"
                    >
                        <line x1="12" y1="5" x2="12" y2="19" />
                        <line x1="5" y1="12" x2="19" y2="12" />
                    </svg>
                </button>
            </form>

            <div class="filters">
                <button
                    v-for="f in filters"
                    :key="f.value"
                    @click="activeFilter = f.value"
                    :class="[
                        'filter-btn',
                        { active: activeFilter === f.value },
                    ]"
                >
                    {{ f.label }}
                    <span class="filter-count">{{ f.count }}</span>
                </button>
            </div>

            <transition-group name="task" tag="div" class="task-list">
                <div
                    v-for="task in filteredTasks"
                    :key="task.id"
                    :class="[
                        'task-card',
                        { done: task.is_done, editing: editingId === task.id },
                    ]"
                >
                    <div v-if="editingId !== task.id" class="task-view">
                        <button
                            @click="toggleDone(task)"
                            :class="['checkbox', { checked: task.is_done }]"
                        >
                            <svg
                                v-if="task.is_done"
                                width="12"
                                height="12"
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                stroke-width="3"
                            >
                                <polyline points="20 6 9 17 4 12" />
                            </svg>
                        </button>
                        <div class="task-body">
                            <p class="task-title">{{ task.title }}</p>
                            <p v-if="task.description" class="task-desc">
                                {{ task.description }}
                            </p>
                        </div>
                        <div class="task-actions">
                            <button
                                @click="startEdit(task)"
                                class="btn-icon btn-edit"
                                title="Изменить"
                            >
                                <svg
                                    width="14"
                                    height="14"
                                    viewBox="0 0 24 24"
                                    fill="none"
                                    stroke="currentColor"
                                    stroke-width="2"
                                >
                                    <path
                                        d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"
                                    />
                                    <path
                                        d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"
                                    />
                                </svg>
                            </button>
                            <button
                                @click="handleDelete(task.id)"
                                class="btn-icon btn-delete"
                                title="Удалить"
                            >
                                <svg
                                    width="14"
                                    height="14"
                                    viewBox="0 0 24 24"
                                    fill="none"
                                    stroke="currentColor"
                                    stroke-width="2"
                                >
                                    <polyline points="3 6 5 6 21 6" />
                                    <path d="M19 6l-1 14H6L5 6" />
                                    <path d="M10 11v6M14 11v6" />
                                    <path d="M9 6V4h6v2" />
                                </svg>
                            </button>
                        </div>
                    </div>

                    <div v-else class="task-edit-form">
                        <input
                            v-model="editTitle"
                            class="edit-input"
                            placeholder="Название"
                        />
                        <input
                            v-model="editDescription"
                            class="edit-input"
                            placeholder="Описание"
                        />
                        <div class="edit-actions">
                            <button
                                @click="handleUpdate(task.id)"
                                class="btn-save"
                            >
                                Сохранить
                            </button>
                            <button
                                @click="editingId = null"
                                class="btn-cancel"
                            >
                                Отмена
                            </button>
                        </div>
                    </div>
                </div>
            </transition-group>

            <div v-if="filteredTasks.length === 0" class="empty">
                <div class="empty-icon">✦</div>
                <p>
                    {{
                        activeFilter === "all"
                            ? "Пока нет задач"
                            : "Нет задач в этой категории"
                    }}
                </p>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";
import { getTasks, createTask, updateTask, deleteTask } from "../api/tasks.js";
import { useAuth } from "../stores/auth.js";

const tasks = ref([]);
const newTitle = ref("");
const newDescription = ref("");
const editingId = ref(null);
const editTitle = ref("");
const editDescription = ref("");
const activeFilter = ref("all");
const router = useRouter();
const { logout } = useAuth();

const filters = computed(() => [
    { value: "all", label: "Все", count: tasks.value.length },
    {
        value: "active",
        label: "Активные",
        count: tasks.value.filter((t) => !t.is_done).length,
    },
    {
        value: "done",
        label: "Готово",
        count: tasks.value.filter((t) => t.is_done).length,
    },
]);

const filteredTasks = computed(() => {
    if (activeFilter.value === "active")
        return tasks.value.filter((t) => !t.is_done);
    if (activeFilter.value === "done")
        return tasks.value.filter((t) => t.is_done);
    return tasks.value;
});

onMounted(async () => {
    const response = await getTasks();
    tasks.value = response.data;
});

const handleCreate = async () => {
    const response = await createTask({
        title: newTitle.value,
        description: newDescription.value || null,
    });
    tasks.value.unshift(response.data);
    newTitle.value = "";
    newDescription.value = "";
};

const handleDelete = async (id) => {
    await deleteTask(id);
    tasks.value = tasks.value.filter((t) => t.id !== id);
};

const startEdit = (task) => {
    editingId.value = task.id;
    editTitle.value = task.title;
    editDescription.value = task.description || "";
};

const handleUpdate = async (id) => {
    const response = await updateTask(id, {
        title: editTitle.value,
        description: editDescription.value || null,
    });
    const index = tasks.value.findIndex((t) => t.id === id);
    tasks.value[index] = response.data;
    editingId.value = null;
};

const toggleDone = async (task) => {
    const response = await updateTask(task.id, { is_done: !task.is_done });
    const index = tasks.value.findIndex((t) => t.id === task.id);
    tasks.value[index] = response.data;
};

const handleLogout = () => {
    logout();
    router.push("/login");
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
    overflow-x: hidden;
}

.bg-orbs {
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 0;
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
    max-width: 680px;
    margin: 0 auto;
    padding: 40px 24px 80px;
}

.header {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    margin-bottom: 40px;
}

.header-left {
    display: flex;
    align-items: baseline;
    gap: 16px;
}

.logo {
    font-family: "Unbounded", sans-serif;
    font-size: 32px;
    font-weight: 600;
    background: linear-gradient(135deg, #c084fc, #f472b6, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -1px;
}

.task-count {
    font-size: 13px;
    color: #6b6880;
    font-weight: 300;
}

.btn-logout {
    display: flex;
    align-items: center;
    gap: 8px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.08);
    color: #9993b0;
    padding: 8px 16px;
    border-radius: 100px;
    font-family: "Onest", sans-serif;
    font-size: 13px;
    cursor: pointer;
    transition: all 0.2s;
}

.btn-logout:hover {
    background: rgba(255, 255, 255, 0.09);
    color: #e8e6f0;
    border-color: rgba(255, 255, 255, 0.15);
}

.create-form {
    display: flex;
    gap: 12px;
    margin-bottom: 24px;
    align-items: flex-start;
}

.input-group {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.input-main,
.input-desc {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 14px 18px;
    font-family: "Onest", sans-serif;
    font-size: 15px;
    color: #e8e6f0;
    outline: none;
    transition: all 0.2s;
    width: 100%;
}

.input-main {
    font-size: 15px;
    font-weight: 500;
}
.input-desc {
    font-size: 13px;
    color: #9993b0;
}

.input-main::placeholder {
    color: #4a4760;
}
.input-desc::placeholder {
    color: #3a3750;
}

.input-main:focus,
.input-desc:focus {
    border-color: rgba(192, 132, 252, 0.4);
    background: rgba(255, 255, 255, 0.07);
    box-shadow: 0 0 0 3px rgba(192, 132, 252, 0.1);
}

.btn-add {
    width: 52px;
    height: 52px;
    background: linear-gradient(135deg, #7c3aed, #db2777);
    border: none;
    border-radius: 14px;
    color: white;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s;
    flex-shrink: 0;
    box-shadow: 0 4px 20px rgba(124, 58, 237, 0.4);
}

.btn-add:hover {
    transform: scale(1.05);
    box-shadow: 0 6px 28px rgba(124, 58, 237, 0.6);
}

.btn-add:active {
    transform: scale(0.97);
}

.filters {
    display: flex;
    gap: 8px;
    margin-bottom: 24px;
}

.filter-btn {
    display: flex;
    align-items: center;
    gap: 6px;
    background: transparent;
    border: 1px solid rgba(255, 255, 255, 0.08);
    color: #6b6880;
    padding: 7px 14px;
    border-radius: 100px;
    font-family: "Onest", sans-serif;
    font-size: 13px;
    cursor: pointer;
    transition: all 0.2s;
}

.filter-btn:hover {
    color: #e8e6f0;
    border-color: rgba(255, 255, 255, 0.15);
}

.filter-btn.active {
    background: rgba(192, 132, 252, 0.15);
    border-color: rgba(192, 132, 252, 0.4);
    color: #c084fc;
}

.filter-count {
    background: rgba(255, 255, 255, 0.08);
    border-radius: 100px;
    padding: 1px 7px;
    font-size: 11px;
}

.filter-btn.active .filter-count {
    background: rgba(192, 132, 252, 0.2);
}

.task-list {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.task-card {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 16px;
    padding: 16px 18px;
    transition: all 0.25s;
    animation: slideIn 0.3s ease;
}

@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateY(-10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.task-card:hover {
    background: rgba(255, 255, 255, 0.06);
    border-color: rgba(255, 255, 255, 0.11);
}

.task-card.done {
    opacity: 0.5;
}

.task-card.editing {
    border-color: rgba(192, 132, 252, 0.3);
    background: rgba(192, 132, 252, 0.05);
}

.task-view {
    display: flex;
    align-items: center;
    gap: 14px;
}

.checkbox {
    width: 22px;
    height: 22px;
    border-radius: 7px;
    border: 1.5px solid rgba(255, 255, 255, 0.15);
    background: transparent;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    transition: all 0.2s;
    color: white;
}

.checkbox:hover {
    border-color: #c084fc;
}

.checkbox.checked {
    background: linear-gradient(135deg, #7c3aed, #db2777);
    border-color: transparent;
    box-shadow: 0 2px 10px rgba(124, 58, 237, 0.4);
}

.task-body {
    flex: 1;
    min-width: 0;
}

.task-title {
    font-size: 15px;
    font-weight: 500;
    color: #e8e6f0;
    transition: all 0.2s;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.done .task-title {
    text-decoration: line-through;
    color: #4a4760;
}

.task-desc {
    font-size: 12px;
    color: #6b6880;
    margin-top: 3px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.task-actions {
    display: flex;
    gap: 6px;
    opacity: 0;
    transition: opacity 0.2s;
}

.task-card:hover .task-actions {
    opacity: 1;
}

.btn-icon {
    width: 32px;
    height: 32px;
    border-radius: 9px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    background: transparent;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.15s;
}

.btn-edit {
    color: #9993b0;
}
.btn-edit:hover {
    background: rgba(192, 132, 252, 0.15);
    border-color: rgba(192, 132, 252, 0.3);
    color: #c084fc;
}

.btn-delete {
    color: #9993b0;
}
.btn-delete:hover {
    background: rgba(239, 68, 68, 0.15);
    border-color: rgba(239, 68, 68, 0.3);
    color: #f87171;
}

.task-edit-form {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.edit-input {
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(192, 132, 252, 0.2);
    border-radius: 10px;
    padding: 10px 14px;
    font-family: "Onest", sans-serif;
    font-size: 14px;
    color: #e8e6f0;
    outline: none;
    transition: all 0.2s;
}

.edit-input:focus {
    border-color: rgba(192, 132, 252, 0.5);
    box-shadow: 0 0 0 3px rgba(192, 132, 252, 0.1);
}

.edit-actions {
    display: flex;
    gap: 8px;
    margin-top: 4px;
}

.btn-save,
.btn-cancel {
    padding: 8px 18px;
    border-radius: 10px;
    border: none;
    font-family: "Onest", sans-serif;
    font-size: 13px;
    cursor: pointer;
    transition: all 0.2s;
}

.btn-save {
    background: linear-gradient(135deg, #7c3aed, #db2777);
    color: white;
    box-shadow: 0 2px 12px rgba(124, 58, 237, 0.3);
}

.btn-save:hover {
    box-shadow: 0 4px 18px rgba(124, 58, 237, 0.5);
    transform: translateY(-1px);
}

.btn-cancel {
    background: rgba(255, 255, 255, 0.06);
    color: #9993b0;
    border: 1px solid rgba(255, 255, 255, 0.08);
}

.btn-cancel:hover {
    background: rgba(255, 255, 255, 0.09);
    color: #e8e6f0;
}

.empty {
    text-align: center;
    padding: 60px 0;
    color: #4a4760;
}

.empty-icon {
    font-size: 32px;
    margin-bottom: 12px;
    background: linear-gradient(135deg, #7c3aed, #db2777);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.empty p {
    font-size: 14px;
    font-weight: 300;
}

.task-enter-active {
    animation: slideIn 0.3s ease;
}
.task-leave-active {
    animation: slideOut 0.25s ease forwards;
}
.task-move {
    transition: transform 0.3s ease;
}

@keyframes slideOut {
    to {
        opacity: 0;
        transform: translateX(20px);
        height: 0;
        margin: 0;
        padding: 0;
    }
}
</style>
