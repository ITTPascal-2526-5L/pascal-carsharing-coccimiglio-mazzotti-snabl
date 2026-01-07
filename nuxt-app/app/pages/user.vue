<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from '#app'

const router = useRouter()
const user = ref<any>(null)

onMounted(() => {
  const userData = localStorage.getItem('user')
  if (userData) {
    user.value = JSON.parse(userData)
  } else {
    router.push('/login')
  }
})

const logout = () => {
  localStorage.removeItem('user')
  router.push('/login')
}
</script>

<template>
  <div>
    <header class="header">
      <div class="container header-inner">
        <div class="brand">
          <span class="brand-badge" aria-hidden="true"></span>
          <span>Car Sharing</span>
        </div>
        <nav class="nav" aria-label="Primary">
          <NuxtLink class="btn" to="/">Home</NuxtLink>
          <button class="btn" @click="logout">Esci</button>
        </nav>
      </div>
    </header>

    <main class="main">
      <div class="container">
        <section v-if="user" class="user-section">
          <article class="card user-card">
            <div class="user-header">
              <div class="avatar-placeholder">
                {{ user.username.charAt(0).toUpperCase() }}
              </div>
              <div class="user-title">
                <h2 class="username">{{ user.username }}</h2>
                <span class="role-badge" :class="user.role">{{ user.role === 'driver' ? 'Conducente' : 'Passeggero' }}</span>
              </div>
            </div>

            <div class="user-details">
              <div class="detail-item">
                <span class="detail-label">Email</span>
                <span class="detail-value">{{ user.email }}</span>
              </div>
              
              <div class="detail-item">
                <span class="detail-label">Telefono</span>
                <span class="detail-value">{{ user.phonenumber }}</span>
              </div>

              <div class="detail-item">
                <span class="detail-label">Età</span>
                <span class="detail-value">{{ user.age }} anni</span>
              </div>

              <div v-if="user.role === 'driver'" class="detail-item">
                <span class="detail-label">Patente</span>
                <span class="detail-value">{{ user.licenseid }}</span>
              </div>

              <div v-if="user.role === 'passenger'" class="detail-item">
                <span class="detail-label">Scuola</span>
                <span class="detail-value">{{ user.attending_school }}</span>
              </div>
            </div>
          </article>
        </section>
      </div>
    </main>

    <footer class="footer">
      <div class="container">
        <small>Coccimiglio Carmine, Samuele Snabl, Mazzotti Alessio</small>
      </div>
    </footer>
  </div>
</template>

<style scoped>
.user-section {
  max-width: 600px;
  margin: 40px auto;
}

.user-card {
  padding: 32px;
}

.user-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 1px solid var(--c-border);
}

.avatar-placeholder {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--c-primary), #3b82f6);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  font-weight: 700;
  color: white;
}

.user-title {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.username {
  font-size: 24px;
  margin: 0;
}

.role-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  width: fit-content;
}

.role-badge.driver {
  background: rgba(14, 165, 233, 0.1);
  color: #0ea5e9;
  border: 1px solid rgba(14, 165, 233, 0.2);
}

.role-badge.passenger {
  background: rgba(168, 85, 247, 0.1);
  color: #a855f7;
  border: 1px solid rgba(168, 85, 247, 0.2);
}

.user-details {
  display: grid;
  gap: 20px;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 8px;
}

.detail-label {
  color: #94a3b8;
  font-size: 14px;
}

.detail-value {
  font-weight: 500;
  color: var(--c-text);
}
</style>
