<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "#app";

const config = useRuntimeConfig();

type FormState = {
  username: string;
  email: string;
  password: string;
  confirmPassword: string;
  role: "passenger" | "driver";
  phonenumber: string;
  age: string;
  licenseid: string;
  attending_school: string;
  license_file: File | null;
};

const router = useRouter();
const state = ref<FormState>({
  username: "",
  email: "",
  password: "",
  confirmPassword: "",
  role: "passenger",
  phonenumber: "",
  age: "",
  licenseid: "",
  attending_school: "",
  license_file: null,
});

const loading = ref(false);
const success = ref(false);
const error = ref("");
const errors = ref<Partial<Record<keyof FormState, string>>>({});

const handleFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files.length > 0) {
    state.value.license_file = target.files[0];
  } else {
    state.value.license_file = null;
  }
};

const validate = (): boolean => {
  errors.value = {};

  const usernameError = schema.username(state.value.username);
  if (usernameError !== true) errors.value.username = usernameError;

  const emailError = schema.email(state.value.email);
  if (emailError !== true) errors.value.email = emailError;

  const passwordError = schema.password(state.value.password);
  if (passwordError !== true) errors.value.password = passwordError;

  const confirmPasswordError = schema.confirmPassword(
    state.value.confirmPassword,
    state.value,
  );
  if (confirmPasswordError !== true)
    errors.value.confirmPassword = confirmPasswordError;

  const phoneError = schema.phonenumber(state.value.phonenumber);
  if (phoneError !== true) errors.value.phonenumber = phoneError;

  const ageError = schema.age(state.value.age);
  if (ageError !== true) errors.value.age = ageError;

  if (state.value.role === "driver") {
    const licenseError = schema.licenseid(state.value.licenseid);
    if (licenseError !== true) errors.value.licenseid = licenseError;

    // Optional: validate file presence if strictly required
    // if (!state.value.license_file) errors.value.license_file = 'License file is required'
  }

  if (state.value.role === "passenger") {
    const schoolError = schema.attending_school(state.value.attending_school);
    if (schoolError !== true) errors.value.attending_school = schoolError;
  }

  return Object.keys(errors.value).length === 0;
};

const schema = {
  username: (v: string) =>
    v?.trim().length >= 3 ? true : "Username must be at least 3 characters",
  email: (v: string) =>
    /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v) ? true : "Invalid email address",
  password: (v: string) => {
    if (!v || v.length < 8) return "Password must be at least 8 characters";
    if (!/[A-Z]/.test(v)) return "Include at least one uppercase letter";
    if (!/[a-z]/.test(v)) return "Include at least one lowercase letter";
    if (!/[0-9]/.test(v)) return "Include at least one number";
    return true;
  },
  confirmPassword: (_: string, form: FormState) =>
    form.password === form.confirmPassword ? true : "Passwords do not match",
  role: (v: string) => (!v ? true : "Please choose a role"),
  phonenumber: (v: string) =>
    v?.trim().length >= 5 ? true : "Phone number is required",
  age: (v: string) => {
    const ageNum = parseInt(v);
    return !isNaN(ageNum) && ageNum >= 18
      ? true
      : "You must be at least 18 years old";
  },
  licenseid: (v: string) =>
    v?.trim().length > 0 ? true : "License ID is required",
  attending_school: (v: string) =>
    v?.trim().length > 0 ? true : "School name is required",
};

const onSubmit = async () => {
  error.value = "";
  errors.value = {};

  if (!validate()) {
    return;
  }

  loading.value = true;
  try {
    const apiUrl = config.public.apiUrl || "http://localhost:5001";

    const formData = new FormData();
    formData.append("username", state.value.username);
    formData.append("email", state.value.email);
    formData.append("password", state.value.password);
    formData.append("role", state.value.role);
    formData.append("phonenumber", state.value.phonenumber);
    formData.append("age", state.value.age);

    if (state.value.role === "driver") {
      formData.append("licenseid", state.value.licenseid);
      if (state.value.license_file) {
        formData.append("license_file", state.value.license_file);
      }
    } else {
      formData.append("attending_school", state.value.attending_school);
    }

    const response = await fetch(`${apiUrl}/api/register`, {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    if (!response.ok) {
      error.value = data.error || "Registration failed. Please try again.";
      return;
    }

    success.value = true;
    setTimeout(() => router.push("/login"), 1200);
  } catch (err) {
    error.value =
      "Network error. Please check if the backend server is running.";
    console.error("Registration error:", err);
  } finally {
    loading.value = false;
  }
};
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
            <h2 class="card-title">Crea un account</h2>
            <p class="card-sub">Registrati come conducente o passeggero</p>

            <form @submit.prevent="onSubmit" class="register-form">
              <!-- Role Selection -->
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

              <!-- Common Fields -->
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
                <span v-if="errors.username" class="error-text">{{
                  errors.username
                }}</span>
              </div>

              <div class="form-group">
                <label for="email" class="label">Email</label>
                <input
                  id="email"
                  v-model="state.email"
                  type="email"
                  class="input"
                  placeholder="tuo@email.com"
                  :class="{ 'input-error': errors.email }"
                  required
                />
                <span v-if="errors.email" class="error-text">{{
                  errors.email
                }}</span>
              </div>

              <div class="form-row">
                <div class="form-group half">
                  <label for="phonenumber" class="label">Telefono</label>
                  <input
                    id="phonenumber"
                    v-model="state.phonenumber"
                    type="tel"
                    class="input"
                    placeholder="+39 333..."
                    :class="{ 'input-error': errors.phonenumber }"
                    required
                  />
                  <span v-if="errors.phonenumber" class="error-text">{{
                    errors.phonenumber
                  }}</span>
                </div>

                <div class="form-group half">
                  <label for="age" class="label">Età</label>
                  <input
                    id="age"
                    v-model="state.age"
                    type="number"
                    min="18"
                    class="input"
                    placeholder="18+"
                    :class="{ 'input-error': errors.age }"
                    required
                  />
                  <span v-if="errors.age" class="error-text">{{
                    errors.age
                  }}</span>
                </div>
              </div>

              <!-- Driver Specific Fields -->
              <div v-if="state.role === 'driver'" class="driver-fields">
                <div class="form-group">
                  <label for="licenseid" class="label">Numero Patente</label>
                  <input
                    id="licenseid"
                    v-model="state.licenseid"
                    type="text"
                    class="input"
                    placeholder="Numero patente"
                    :class="{ 'input-error': errors.licenseid }"
                    required
                  />
                  <span v-if="errors.licenseid" class="error-text">{{
                    errors.licenseid
                  }}</span>
                </div>

                <div class="form-group">
                  <label for="license_file" class="label"
                    >Carica Patente (PDF/IMG)</label
                  >
                  <input
                    id="license_file"
                    type="file"
                    accept=".pdf,.png,.jpg,.jpeg"
                    class="input file-input"
                    @change="handleFileChange"
                  />
                </div>
              </div>

              <!-- Passenger Specific Fields -->
              <div v-if="state.role === 'passenger'" class="passenger-fields">
                <div class="form-group">
                  <label for="attending_school" class="label"
                    >Scuola Frequentata</label
                  >
                  <input
                    id="attending_school"
                    v-model="state.attending_school"
                    type="text"
                    class="input"
                    placeholder="Nome della scuola"
                    :class="{ 'input-error': errors.attending_school }"
                    required
                  />
                  <span v-if="errors.attending_school" class="error-text">{{
                    errors.attending_school
                  }}</span>
                </div>
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
                <span v-if="errors.password" class="error-text">{{
                  errors.password
                }}</span>
              </div>

              <div class="form-group">
                <label for="confirmPassword" class="label"
                  >Conferma Password</label
                >
                <input
                  id="confirmPassword"
                  v-model="state.confirmPassword"
                  type="password"
                  class="input"
                  placeholder="Conferma la tua password"
                  :class="{ 'input-error': errors.confirmPassword }"
                  required
                />
                <span v-if="errors.confirmPassword" class="error-text">{{
                  errors.confirmPassword
                }}</span>
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

.form-row {
  display: flex;
  gap: 12px;
}

.half {
  flex: 1;
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

.file-input {
  padding: 8px;
  background: #1e293b;
}
</style>
