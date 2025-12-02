<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from '#app'

const config = useRuntimeConfig()
const router = useRouter()

const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

const onSubmit = async () => {
  error.value = ''
  loading.value = true
  
  try {
    const apiUrl = config.public.apiUrl || 'http://localhost:5001'
    const response = await fetch(`${apiUrl}/api/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: username.value,
        password: password.value
      })
    })
    
    const data = await response.json()
    
    if (!response.ok) {
      error.value = data.error || 'Login failed'
      return
    }
    
    // Store user data and token
    const token = useCookie('auth_token')
    token.value = data.access_token
    
    if (process.client) {
      localStorage.setItem('user', JSON.stringify(data.user))
    }
    
    router.push('/user')
    
  } catch (err) {
    error.value = 'Network error. Please check if the backend server is running.'
    console.error('Login error:', err)
  } finally {
    loading.value = false
  }
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
          <NuxtLink class="btn" to="/register">Registrati</NuxtLink>
          <NuxtLink class="btn" to="/register-school">Scuole</NuxtLink>
          <NuxtLink class="btn primary" to="/login">Accedi</NuxtLink>
        </nav>
      </div>
    </header>

    <main class="main">
      <div class="container">
        <section class="login-section">
          <article class="card login-card">
            <h2 class="card-title">Bentornato</h2>
            <p class="card-sub">Accedi al tuo account</p>
            
            <form @submit.prevent="onSubmit" class="login-form">
              <div class="form-group">
                <label for="username" class="label">Username</label>
                <input
                  id="username"
                  v-model="username"
                  type="text"
                  class="input"
                  placeholder="Il tuo username"
                  required
                />
              </div>

              <div class="form-group">
                <label for="password" class="label">Password</label>
                <input
                  id="password"
                  v-model="password"
                  type="password"
                  class="input"
                  placeholder="La tua password"
                  required
                />
              </div>

              <div v-if="error" class="error-message">
                {{ error }}
              </div>

              <button
                type="submit"
                class="btn primary submit-btn"
                :disabled="loading"
              >
                <span v-if="loading">Accesso in corso...</span>
                <span v-else>Accedi</span>
              </button>
            </form>
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
.login-section {
  max-width: 400px;
  margin: 40px auto;
}

.login-card {
  padding: 32px;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-top: 24px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.label {
  font-size: 14px;
  font-weight: 600;
  color: var(--c-text);
}

.error-message {
  padding: 12px;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: 8px;
  color: #ef4444;
  font-size: 14px;
}

.submit-btn {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  margin-top: 8px;
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
