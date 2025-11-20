<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from '#app'

const config = useRuntimeConfig()

type FormState = {
  username: string
  password: string
  confirmPassword: string
  role: 'passenger' | 'driver'
}

const router = useRouter()
const state = ref<FormState>({
  username: '',
  password: '',
  confirmPassword: '',
  role: 'passenger'
})

const loading = ref(false)
const success = ref(false)
const error = ref('')
const errors = ref<Partial<Record<keyof FormState, string>>>({})

const validate = (): boolean => {
  errors.value = {}
  
  const usernameError = schema.username(state.value.username)
  if (usernameError !== true) {
    errors.value.username = usernameError
  }
  
  const passwordError = schema.password(state.value.password)
  if (passwordError !== true) {
    errors.value.password = passwordError
  }
  
  const confirmPasswordError = schema.confirmPassword(state.value.confirmPassword, state.value)
  if (confirmPasswordError !== true) {
    errors.value.confirmPassword = confirmPasswordError
  }
  
  return Object.keys(errors.value).length === 0
}

const schema = {
  username: (v: string) => (v?.trim().length >= 3 ? true : 'Username must be at least 3 characters'),
  password: (v: string) => {
    if (!v || v.length < 8) return 'Password must be at least 8 characters'
    if (!/[A-Z]/.test(v)) return 'Include at least one uppercase letter'
    if (!/[a-z]/.test(v)) return 'Include at least one lowercase letter'
    if (!/[0-9]/.test(v)) return 'Include at least one number'
    return true
  },
  confirmPassword: (_: string, form: FormState) =>
    form.password === form.confirmPassword ? true : 'Passwords do not match',
  role: (v: string) => (!!v ? true : 'Please choose a role')
}

const onSubmit = async () => {
  error.value = ''
  errors.value = {}
  
  if (!validate()) {
    return
  }
  
  loading.value = true
  try {
    const apiUrl = config.public.apiUrl || 'http://localhost:5000'
    const response = await fetch(`${apiUrl}/api/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: state.value.username,
        password: state.value.password,
        role: state.value.role
      })
    })
    
    const data = await response.json()
    
    if (!response.ok) {
      error.value = data.error || 'Registration failed. Please try again.'
      return
    }
    
    success.value = true
    setTimeout(() => router.push('/login'), 1200)
  } catch (err) {
    error.value = 'Network error. Please check if the backend server is running.'
    console.error('Registration error:', err)
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
          <NuxtLink class="btn primary" to="/login">Accedi</NuxtLink>
        </nav>
      </div>
    </header>

    <main class="main">
      <div class="container">
        <section class="register-section">
          <article class="card register-card">
            <h2 class="card-title">Crea un account</h2>
            <p class="card-sub">Registrati come conducente o passeggero</p>
            
            <form @submit.prevent="onSubmit" class="register-form">
              <div class="form-group">
                <label for="username" class="label">Username</label>
                <input
                  id="username"
                  v-model="state.username"
                  type="text"
                  class="input"
                  placeholder="Inserisci il tuo username"
                  :class="{ 'input-error': errors.username }"
                  required
                />
                <span v-if="errors.username" class="error-text">{{ errors.username }}</span>
              </div>

              <div class="form-group">
                <label for="password" class="label">Password</label>
                <input
                  id="password"
                  v-model="state.password"
                  type="password"
                  class="input"
                  placeholder="Inserisci la tua password"
                  :class="{ 'input-error': errors.password }"
                  required
                />
                <span v-if="errors.password" class="error-text">{{ errors.password }}</span>
              </div>

              <div class="form-group">
                <label for="confirmPassword" class="label">Conferma Password</label>
                <input
                  id="confirmPassword"
                  v-model="state.confirmPassword"
                  type="password"
                  class="input"
                  placeholder="Conferma la tua password"
                  :class="{ 'input-error': errors.confirmPassword }"
                  required
                />
                <span v-if="errors.confirmPassword" class="error-text">{{ errors.confirmPassword }}</span>
              </div>

              <div class="form-group">
                <label class="label">Ruolo</label>
                <div class="role-selector">
                  <label class="role-option">
                    <input
                      type="radio"
                      v-model="state.role"
                      value="passenger"
                      class="radio-input"
                    />
                    <span class="radio-label">Passeggero</span>
                  </label>
                  <label class="role-option">
                    <input
                      type="radio"
                      v-model="state.role"
                      value="driver"
                      class="radio-input"
                    />
                    <span class="radio-label">Conducente</span>
                  </label>
                </div>
              </div>

              <div v-if="error" class="error-message">
                {{ error }}
              </div>

              <div v-if="success" class="success-message">
                Registrazione completata con successo!
              </div>

              <button
                type="submit"
                class="btn primary submit-btn"
                :disabled="loading"
              >
                <span v-if="loading">Registrazione in corso...</span>
                <span v-else>Registrati</span>
              </button>
            </form>
          </article>
        </section>
      </div>
    </main>

    <footer class="footer">
      <div class="container">
        <small>© {{ new Date().getFullYear() }} Car Sharing. Tutti i diritti riservati.</small>
      </div>
    </footer>
  </div>
</template>


<style scoped>
.register-section {
  max-width: 500px;
  margin: 0 auto;
}

.register-card {
  grid-column: span 12;
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.label {
  font-size: 14px;
  font-weight: 600;
  color: var(--c-text);
}

.input-error {
  border-color: #ef4444 !important;
}

.error-text {
  font-size: 12px;
  color: #ef4444;
  margin-top: -4px;
}

.error-message {
  padding: 12px;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: 8px;
  color: #ef4444;
  font-size: 14px;
}

.success-message {
  padding: 12px;
  background: rgba(34, 197, 94, 0.1);
  border: 1px solid rgba(34, 197, 94, 0.3);
  border-radius: 8px;
  color: #22c55e;
  font-size: 14px;
}

.role-selector {
  display: flex;
  gap: 12px;
}

.role-option {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 14px;
  border: 1px solid var(--c-border);
  border-radius: 10px;
  background: #0a1324;
  cursor: pointer;
  transition: all 0.2s ease;
  flex: 1;
}

.role-option:hover {
  border-color: #334155;
  background: rgba(14, 165, 233, 0.05);
}

.role-option input[type="radio"]:checked + .radio-label {
  color: var(--c-primary);
  font-weight: 600;
}

.radio-input {
  margin: 0;
  cursor: pointer;
}

.radio-label {
  cursor: pointer;
  user-select: none;
}

.submit-btn {
  margin-top: 8px;
  width: 100%;
  padding: 12px;
  font-size: 16px;
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none !important;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity .15s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>