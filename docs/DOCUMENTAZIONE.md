# Documentazione Completa - Pascal Car Sharing

## 1. Panoramica del Progetto

**Pascal Car Sharing** è una piattaforma web completa per la gestione del car sharing scolastico, progettata per connettere conducenti (studenti maggiorenni/personale) e passeggeri. Il sistema è costruito con un'architettura moderna separata (Frontend e Backend) per garantire scalabilità e manutenibilità.

### Stack Tecnologico

*   **Backend**: Python con **Flask** (Microframework).
*   **Frontend**: TypeScript con **Nuxt 3** (Framework Vue.js).
*   **Database**: Ibrido.
    *   Definizione modelli: **SQLAlchemy** (ORM).
    *   Persistenza attuale: **File JSON** (drivers.json, passengers.json, schools.json) per semplicità di deployment iniziale e testing.
*   **Autenticazione**: JSON Web Tokens (JWT) tramite `flask-jwt-extended`.

---

## 2. Architettura Backend (`app/`)

Il backend espone servizi REST API consumati dal frontend. Segue il pattern "Application Factory" di Flask per una migliore organizzazione e testabilità.

### Modelli Dati (Data Models)

Sebbene il sistema utilizzi file JSON per il salvataggio effettivo in questa fase, i modelli sono strutturati rigorosamente tramite classi SQLAlchemy.

#### 1. Driver (`app/models/driver.py`)
Rappresenta un conducente autorizzato.
*   **Campi**:
    *   `id`: Integer (Primary Key)
    *   `name`, `surname`: String (Obbligatori)
    *   `age`: Integer
    *   `email`: String (Univoca)
    *   `phonenumber`: String (Univoco)
    *   `password_hash`: String (Hash di sicurezza)
    *   `licenseid`: String (Numero patente, Univoco)
    *   `rating`: Float (Valutazione media)
    *   `priceperkm`: Float (Tariffa al km)
    *   `created_at`: DateTime

#### 2. Passenger (`app/models/passenger.py`)
Rappresenta un utente che usufruisce dei passaggi.
*   **Campi**:
    *   `id`: Integer (Primary Key)
    *   `name`, `surname`: String
    *   `email`, `phonenumber`: String
    *   `school_id`: Integer (ForeignKey verso School)
    *   `created_at`: DateTime

#### 3. School (`app/models/school.py`)
Rappresenta gli istituti scolastici aderenti.

### API Endpoints

#### Autenticazione (`app/routes/login.py`)

*   **POST** `/api/login`
    *   **Input**: JSON `{ "username": "...", "password": "..." }`
    *   **Logica**:
        1.  Cerca l'utente in `drivers.json`.
        2.  Se non trovato, cerca in `passengers.json`.
        3.  Verifica l'hash della password (`werkzeug.security.check_password_hash`).
        4.  Genera un **JWT Access Token**.
    *   **Output**: `{ "access_token": "...", "user": { ...dati_utente... } }`

*   **POST** `/api/logout`
    *   Endpoint placeholder per futura invalidazione token (blacklist).

*   **GET** `/api/protected` (Richiede Header `Authorization: Bearer <token>`)
    *   Endpoint di test per verificare la validità del token.

#### Registrazione (`app/routes/register.py`)

*   **POST** `/api/register`
    *   Gestisce la registrazione sia di Driver che di Passenger.
    *   Supporta `multipart/form-data` per l'upload della patente (solo Driver).
    *   **Validazioni**:
        *   Email > 5 caratteri.
        *   Password > 8 caratteri.
        *   Nome/Cognome > 3 caratteri.
        *   Controllo esistenza email duplicata.
    *   **Persistenza**: Scrive i dati in `drivers.json` o `passengers.json`.

*   **POST** `/api/register-school`
    *   Permette la registrazione di un nuovo istituto scolastico.
    *   Campi: `school_name`, `address`, `email`, `representative`, `mechanical_code`.
    *   Salva in `schools.json`.

---

## 3. Architettura Frontend (`nuxt-app/`)

Il frontend è una Single Page Application (SPA) moderna realizzata con Nuxt 3.

### Configurazione (`nuxt.config.ts`)

*   **Runtime Config**:
    *   `public.apiUrl`: Punta al backend Flask (default: `http://127.0.0.1:5001`).
*   **CSS Globali**: Importa font Google (Inter) e definisce variabili CSS per i colori (`--c-primary`, `--c-text`, ecc) in `global.css`.

### Componenti Chiave

#### Pagina di Registrazione (`Register.vue`)
*   Utilizza la **Composition API** di Vue 3 (`<script setup lang="ts">`).
*   **Stato**: Gestisce i campi del form, errori e caricamento tramite `ref`.
*   **Validazione Client-side**:
    *   Schema di validazione personalizzato per username, password (complessità) e corrispondenza password.
*   **Network**: Invia una richiesta POST al backend e gestisce il redirect al login in caso di successo.

---

## 4. Gestione Dati e Persistenza

Il progetto adotta un approccio ibrido transitorio.

1.  **Storage**: I dati non risiedono in un database relazionale attivo (es. PostgreSQL/SQLite file), ma vengono serializzati in file di testo JSON-Line (`.json`).
    *   `drivers.json`
    *   `passengers.json`
    *   `schools.json`
2.  **Testing**: Quando l'applicazione gira in modalità TEST, vengono utilizzati file separati (`test_drivers.json`, ecc.) per non corrompere i dati reali.

---

## 5. Installazione e Avvio

### Backend
1.  Posizionarsi nella root del progetto.
2.  Creare virtual environment: `python -m venv venv`.
3.  Attivare environment (Windows: `venv\Scripts\activate`).
4.  Installare dipendenze: `pip install -r requirements.txt`.
5.  Avviare server: `python app.py` (Default port: 5001).

### Frontend
1.  Posizionarsi in `nuxt-app/`.
2.  Installare pacchetti: `npm install`.
3.  Avviare server di sviluppo: `npm run dev`.
4.  Accedere a `http://localhost:3000`.