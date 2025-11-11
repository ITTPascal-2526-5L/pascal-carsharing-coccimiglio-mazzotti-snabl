<script setup lang="ts">
// Homepage component
</script>

<template>
  <div style="min-height: 100vh; padding: 20px;">
    <h1 style="color: #0ea5e9; font-size: 2rem; margin-bottom: 20px;">Car Sharing - Homepage</h1>
    <p style="color: #e5e7eb; margin-bottom: 20px;">Benvenuto nel servizio di car sharing</p>
    
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
        <section class="grid">
          <article class="card">
            <h2 class="card-title">Trova un'auto</h2>
            <p class="card-sub">Prenota in pochi secondi con tariffe chiare.</p>
            <div class="input-row">
              <input class="input" type="text" placeholder="Città o indirizzo" aria-label="Città o indirizzo" />
              <input class="input" type="datetime-local" aria-label="Data e ora di inizio" />
              <button class="btn primary">Cerca</button>
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

