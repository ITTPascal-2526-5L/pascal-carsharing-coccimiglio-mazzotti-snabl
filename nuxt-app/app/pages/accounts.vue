<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'

const config = useRuntimeConfig()

type User = {
  username?: string
  name?: string
  surname?: string
  email: string
  phonenumber?: string
  age?: string | number
  licenseid?: string
  attending_school?: string
  role: 'driver' | 'passenger'
  created_at?: string
}

const users = ref<User[]>([])
const loading = ref(false)
const error = ref('')

const sortedUsers = computed(() =>
  [...users.value].sort((a, b) => {
    const aDate = a.created_at ? new Date(a.created_at).getTime() : 0
    const bDate = b.created_at ? new Date(b.created_at).getTime() : 0
    return bDate - aDate
  })
)

const fetchUsers = async () => {
  loading.value = true
  error.value = ''

  try {
    const apiUrl = config.public.apiUrl || 'http://localhost:5001'
    const response = await fetch(`${apiUrl}/api/users`)
    const data = await response.json()

    if (!response.ok) {
      error.value = data.error || 'Impossibile caricare gli utenti.'
      return
    }

    users.value = data.users || []
  } catch (err) {
    console.error('Errore caricamento utenti:', err)
    error.value =
      'Errore di rete. Verifica che il server backend sia in esecuzione.'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchUsers()
})
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
          <NuxtLink class="btn" to="/login">Accedi</NuxtLink>
        </nav>
      </div>
    </header>

    <main class="main">
      <div class="container">
        <section class="accounts-section">
          <article class="card accounts-card">
            <div class="accounts-header">
              <div>
                <h2 class="card-title">Account registrati</h2>
                <p class="card-sub">
                  Elenco di tutti gli utenti registrati al servizio.
                </p>
              </div>
              <span class="badge" v-if="!loading">
                Totale: {{ users.length }}
              </span>
            </div>

            <div v-if="error" class="error-message">
              {{ error }}
            </div>

            <div v-else>
              <div v-if="loading" class="loading-row">
                Caricamento utenti...
              </div>

              <div v-else-if="sortedUsers.length === 0" class="empty-state">
                Nessun utente registrato al momento.
              </div>

              <div v-else class="table-wrapper">
                <table class="accounts-table">
                  <thead>
                    <tr>
                      <th>Ruolo</th>
                      <th>Username / Nome</th>
                      <th>Email</th>
                      <th>Telefono</th>
                      <th>Età</th>
                      <th v-if="true">Dettagli</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="user in sortedUsers" :key="user.email + user.role">
                      <td>
                        <span
                          class="role-chip"
                          :class="user.role === 'driver' ? 'driver' : 'passenger'"
                        >
                          {{ user.role === 'driver' ? 'Conducente' : 'Passeggero' }}
                        </span>
                      </td>
                      <td>
                        <div class="user-cell">
                          <span class="user-main">
                            {{ user.username || `${user.name ?? ''} ${user.surname ?? ''}`.trim() || 'N/D' }}
                          </span>
                          <span class="user-sub" v-if="user.name || user.surname">
                            {{ [user.name, user.surname].filter(Boolean).join(' ') }}
                          </span>
                        </div>
                      </td>
                      <td>{{ user.email }}</td>
                      <td>{{ user.phonenumber || '—' }}</td>
                      <td>{{ user.age || '—' }}</td>
                      <td>
                        <span v-if="user.role === 'driver'">
                          Patente: {{ user.licenseid || '—' }}
                        </span>
                        <span v-else>
                          Scuola: {{ user.attending_school || '—' }}
                        </span>
                      </td>
                    </tr>
                  </tbody>
                </table>
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
.accounts-section {
  margin: 40px auto;
}

.accounts-card {
  padding: 24px;
}

.accounts-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.badge {
  padding: 4px 10px;
  border-radius: 999px;
  background: rgba(148, 163, 184, 0.15);
  border: 1px solid rgba(148, 163, 184, 0.4);
  font-size: 12px;
  color: #e5e7eb;
}

.table-wrapper {
  margin-top: 12px;
  border-radius: 12px;
  overflow: auto;
  border: 1px solid rgba(15, 23, 42, 0.9);
}

.accounts-table {
  width: 100%;
  border-collapse: collapse;
  min-width: 720px;
  background: radial-gradient(circle at top left, #020617, #020617);
}

.accounts-table thead {
  background: rgba(15, 23, 42, 0.9);
}

.accounts-table th,
.accounts-table td {
  padding: 10px 12px;
  text-align: left;
  font-size: 14px;
  border-bottom: 1px solid rgba(30, 64, 175, 0.25);
}

.accounts-table th {
  font-weight: 600;
  color: #cbd5f5;
  position: sticky;
  top: 0;
  z-index: 1;
}

.accounts-table tbody tr:nth-child(even) {
  background: rgba(15, 23, 42, 0.65);
}

.accounts-table tbody tr:nth-child(odd) {
  background: rgba(15, 23, 42, 0.8);
}

.role-chip {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
}

.role-chip.driver {
  background: rgba(56, 189, 248, 0.12);
  border: 1px solid rgba(56, 189, 248, 0.25);
  color: #38bdf8;
}

.role-chip.passenger {
  background: rgba(244, 114, 182, 0.12);
  border: 1px solid rgba(244, 114, 182, 0.25);
  color: #f472b6;
}

.user-cell {
  display: flex;
  flex-direction: column;
}

.user-main {
  font-weight: 500;
}

.user-sub {
  font-size: 12px;
  color: #9ca3af;
}

.loading-row,
.empty-state {
  padding: 16px;
  text-align: center;
  color: #9ca3af;
}

.error-message {
  padding: 12px;
  margin-bottom: 8px;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.35);
  border-radius: 8px;
  color: #fecaca;
  font-size: 14px;
}
</style>


