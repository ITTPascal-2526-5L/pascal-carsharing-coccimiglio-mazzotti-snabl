<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from '#app'

const config = useRuntimeConfig()
const router = useRouter()

type SchoolFormState = {
  school_name: string
  address: string
  email: string
  representative: string
  codice_meccanografico: string
}

const state = ref<SchoolFormState>({
  school_name: '',
  address: '',
  email: '',
  representative: '',
  codice_meccanografico: ''
})

const loading = ref(false)
const success = ref(false)
const error = ref('')

const onSubmit = async () => {
  error.value = ''
  loading.value = true
  
  try {
    const apiUrl = config.public.apiUrl || 'http://localhost:5001'
    const response = await fetch(`${apiUrl}/api/register-school`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(state.value)
    })
    
    const data = await response.json()
    
    if (!response.ok) {
      error.value = data.error || 'Application failed. Please try again.'
      return
    }
    
    success.value = true
    // Reset form
    state.value = {
      school_name: '',
      address: '',
      email: '',
      representative: '',
      codice_meccanografico: ''
    }
    
  } catch (err) {
    error.value = 'Network error. Please check if the backend server is running.'
    console.error('School registration error:', err)
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
        <section class="register-section">
          <article class="card register-card">
            <h2 class="card-title">Candidatura Scuola</h2>
            <p class="card-sub">Registra il tuo istituto al servizio di Car Sharing</p>
            
            <form @submit.prevent="onSubmit" class="register-form">
              <div class="form-group">
                <label for="school_name" class="label">Nome Scuola</label>
                <input
                  id="school_name"
                  v-model="state.school_name"
                  type="text"
                  class="input"
                  placeholder="Istituto Tecnico..."
                  required
                />
              </div>

              <div class="form-group">
                <label for="codice_meccanografico" class="label">Codice Meccanografico</label>
                <input
                  id="codice_meccanografico"
                  v-model="state.codice_meccanografico"
                  type="text"
                  class="input"
                  placeholder="MIMM00000X"
                  required
                />
              </div>

              <div class="form-group">
                <label for="address" class="label">Indirizzo</label>
                <input
                  id="address"
                  v-model="state.address"
                  type="text"
                  class="input"
                  placeholder="Via Roma 1, Milano"
                  required
                />
              </div>

              <div class="form-group">
                <label for="email" class="label">Email Istituzionale</label>
                <input
                  id="email"
                  v-model="state.email"
                  type="email"
                  class="input"
                  placeholder="segreteria@scuola.it"
                  required
                />
              </div>

              <div class="form-group">
                <label for="representative" class="label">Rappresentante Legale</label>
                <input
                  id="representative"
                  v-model="state.representative"
                  type="text"
                  class="input"
                  placeholder="Nome e Cognome"
                  required
                />
              </div>

              <div v-if="error" class="error-message">
                {{ error }}
              </div>

              <div v-if="success" class="success-message">
                Candidatura inviata con successo! Verrete ricontattati presto.
              </div>

              <button
                type="submit"
                class="btn primary submit-btn"
                :disabled="loading"
              >
                <span v-if="loading">Invio in corso...</span>
                <span v-else>Invia Candidatura</span>
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

.submit-btn {
  margin-top: 8px;
  width: 100%;
  padding: 12px;
  font-size: 16px;
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
