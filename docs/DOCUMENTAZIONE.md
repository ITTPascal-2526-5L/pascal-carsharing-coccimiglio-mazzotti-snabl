# Documentazione Progetto Pascal Car Sharing

## Indice
1. [Panoramica del Progetto](#panoramica-del-progetto)
2. [Architettura del Sistema](#architettura-del-sistema)
3. [Documentazione delle Feature](#documentazione-delle-feature)
4. [Diagramma delle Classi](#diagramma-delle-classi)
5. [Test](#test)
6. [Installazione e Configurazione](#installazione-e-configurazione)

---

## Panoramica del Progetto

**Pascal Car Sharing** è un sistema di car sharing che permette a conducenti e passeggeri di registrarsi e utilizzare il servizio. Il progetto è sviluppato con un'architettura full-stack:

- **Backend**: Flask (Python) - API REST
- **Frontend**: Nuxt.js (Vue.js) - Interfaccia utente moderna
- **Storage**: File JSON per la persistenza dei dati (soluzione temporanea)

---

## Architettura del Sistema

### Backend (Flask)

Il backend è organizzato seguendo il pattern **Application Factory** di Flask:

```
app/
├── __init__.py          # Factory per creare l'applicazione Flask
├── config.py            # Configurazione dell'applicazione
├── models/              # Modelli di dati
│   ├── __init__.py
│   └── user.py          # Modelli User, Driver, Passenger
└── routes/              # Blueprint per le route
    ├── __init__.py
    ├── main.py          # Route principali
    └── register.py      # Route per la registrazione
```

### Frontend (Nuxt.js)

Il frontend utilizza Nuxt 3 con Vue 3:

```
nuxt-app/
├── app/
│   ├── app.vue          # Componente root
│   └── global.css       # Stili globali
├── pages/               # Routing automatico
│   ├── index.vue        # Homepage
│   └── register.vue     # Pagina di registrazione
└── nuxt.config.ts       # Configurazione Nuxt
```

---

## Documentazione delle Feature

### 1. Registrazione Utenti

#### Descrizione
La feature di registrazione permette a nuovi utenti (conducenti o passeggeri) di creare un account nel sistema. Il sistema valida i dati inseriti, verifica l'unicità dello username e salva le credenziali in modo sicuro.

#### Come è stata realizzata

**Backend (`app/routes/register.py`)**:
- Endpoint REST: `POST /api/register`
- Accetta dati JSON con: `username`, `password`, `role`
- Validazione:
  - Username minimo 3 caratteri
  - Password minimo 8 caratteri
  - Role deve essere 'driver' o 'passenger'
- Verifica duplicati: controlla se lo username esiste già
- Hash password: utilizza `werkzeug.security.generate_password_hash`
- Persistenza: salva in `drivers.json` o `passengers.json` (formato JSONL)

**Frontend (`nuxt-app/pages/register.vue`)**:
- Form reattivo con Vue 3 Composition API
- Validazione lato client:
  - Username: minimo 3 caratteri
  - Password: minimo 8 caratteri, deve contenere maiuscole, minuscole e numeri
  - Conferma password: deve corrispondere
- Feedback visivo: errori, successo, loading state
- Chiamata API: fetch verso `http://localhost:5000/api/register`

#### Componenti coinvolti

**Backend**:
- `app/routes/register.py`: Blueprint con endpoint `/api/register`
- `app/models/user.py`: Modelli User, Driver, Passenger (per future estensioni)
- `app/__init__.py`: Configurazione CORS per permettere richieste cross-origin

**Frontend**:
- `nuxt-app/pages/register.vue`: Componente pagina di registrazione
- `nuxt-app/app/global.css`: Stili per il form
- `nuxt-app/nuxt.config.ts`: Configurazione API URL

#### Flusso di esecuzione

1. Utente compila il form di registrazione
2. Frontend valida i dati lato client
3. Frontend invia richiesta POST a `/api/register`
4. Backend valida i dati ricevuti
5. Backend verifica se lo username esiste già
6. Backend genera hash della password
7. Backend salva i dati nel file JSON appropriato
8. Backend restituisce risposta JSON con esito
9. Frontend mostra messaggio di successo/errore
10. In caso di successo, redirect a `/login` dopo 1.2 secondi

---

### 2. Homepage

#### Descrizione
La homepage fornisce un'interfaccia iniziale per gli utenti, con navigazione e un form di ricerca base per trovare auto disponibili.

#### Come è stata realizzata

**Backend (`app/routes/main.py`)**:
- Endpoint: `GET /`
- Restituisce template HTML (per compatibilità con vecchio sistema)

**Frontend (`nuxt-app/pages/index.vue`)**:
- Pagina statica con header, form di ricerca e footer
- Form di ricerca (non ancora funzionale, placeholder per future feature)
- Navigazione con link a Register e Login

#### Componenti coinvolti

- `app/routes/main.py`: Blueprint principale
- `nuxt-app/pages/index.vue`: Componente homepage
- `nuxt-app/app/global.css`: Stili condivisi

---

### 3. Configurazione CORS

#### Descrizione
Il sistema è configurato per permettere comunicazione tra frontend (porta 3000) e backend (porta 5000) attraverso CORS (Cross-Origin Resource Sharing).

#### Come è stata realizzata

**Backend (`app/__init__.py`)**:
- Utilizza `flask-cors` per gestire CORS
- Configurazione per route `/api/*`:
  - Origins: `*` (in sviluppo, da restringere in produzione)
  - Methods: GET, POST, PUT, DELETE, OPTIONS
  - Headers: Content-Type, Authorization

#### Componenti coinvolti

- `app/__init__.py`: Configurazione CORS nell'application factory
- `requirements.txt`: Dipendenza `flask-cors==5.0.0`

---

## Diagramma delle Classi

### Struttura delle Classi

```
┌─────────────────────────────────────────────────────────────┐
│                         User                                 │
├─────────────────────────────────────────────────────────────┤
│ - username: str                                              │
│ - password_hash: str                                         │
│ - user_type: str                                             │
├─────────────────────────────────────────────────────────────┤
│ + check_password(password: str) -> bool                     │
│ + to_dict() -> dict                                          │
│ + from_dict(data: dict) -> User                              │
│ + hash_password(password: str) -> str                        │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │
                    ┌─────────┴─────────┐
                    │                   │
        ┌───────────┴──────┐  ┌────────┴──────────┐
        │     Driver       │  │    Passenger     │
        ├──────────────────┤  ├──────────────────┤
        │ (user_type='driver')│ │(user_type='passenger')│
        └──────────────────┘  └──────────────────┘
```

### Dettaglio delle Classi

#### Classe `User`

**Ruolo**: Classe base astratta per rappresentare un utente del sistema.

**Attributi**:
- `username` (str): Nome utente univoco nel sistema
- `password_hash` (str): Hash della password (non password in chiaro)
- `user_type` (str): Tipo di utente, può essere 'driver' o 'passenger'

**Metodi**:
- `check_password(password: str) -> bool`: Verifica se una password corrisponde all'hash salvato. Utilizza `werkzeug.security.check_password_hash`.
- `to_dict() -> dict`: Serializza l'utente in un dizionario per la persistenza.
- `from_dict(data: dict) -> User`: Deserializza un dizionario in un oggetto User (metodo di classe).
- `hash_password(password: str) -> str`: Genera l'hash di una password (metodo statico). Utilizza `werkzeug.security.generate_password_hash`.

**Interazioni**:
- Viene utilizzata come base per `Driver` e `Passenger`
- I dati vengono serializzati/deserializzati per la persistenza in JSON
- La classe interagisce con `werkzeug.security` per la gestione sicura delle password

#### Classe `Driver`

**Ruolo**: Rappresenta un conducente del sistema.

**Attributi**: Eredita tutti gli attributi da `User`.

**Metodi**: Eredita tutti i metodi da `User`.

**Comportamento specifico**:
- Nel `__post_init__`, imposta automaticamente `user_type = 'driver'`
- Chiama `super().__post_init__()` per validare il tipo

**Interazioni**:
- Eredita da `User`
- I dati vengono salvati in `drivers.json`

#### Classe `Passenger`

**Ruolo**: Rappresenta un passeggero del sistema.

**Attributi**: Eredita tutti gli attributi da `User`.

**Metodi**: Eredita tutti i metodi da `User`.

**Comportamento specifico**:
- Nel `__post_init__`, imposta automaticamente `user_type = 'passenger'`
- Chiama `super().__post_init__()` per validare il tipo

**Interazioni**:
- Eredita da `User`
- I dati vengono salvati in `passengers.json`

### Relazioni tra Classi

1. **Ereditarietà**: `Driver` e `Passenger` ereditano da `User` (relazione IS-A)
2. **Composizione**: Le classi utilizzano `werkzeug.security` per la gestione delle password
3. **Serializzazione**: Le classi possono essere convertite in dizionari per la persistenza

### Note di Implementazione

- Le classi utilizzano `@dataclass` per semplificare la definizione
- La validazione avviene in `__post_init__`
- Le password non vengono mai salvate in chiaro, solo come hash
- La persistenza attuale è su file JSON, ma le classi sono progettate per essere facilmente adattabili a un database

---

## Test

### Struttura dei Test

I test sono organizzati nella cartella `tests/` seguendo la struttura del progetto:

```
tests/
├── __init__.py
├── test_models.py          # Test per i modelli
├── test_register.py         # Test per la registrazione
└── conftest.py              # Configurazione pytest
```

### Test dei Modelli

#### Test Classe `User`

**Test `test_user_creation`**:
- Verifica la creazione corretta di un utente
- Controlla che gli attributi siano impostati correttamente

**Test `test_user_password_hashing`**:
- Verifica che le password vengano hashate correttamente
- Controlla che `hash_password` generi hash diversi per password diverse

**Test `test_user_check_password`**:
- Verifica che `check_password` funzioni correttamente
- Testa password corrette e errate

**Test `test_user_serialization`**:
- Verifica `to_dict()` e `from_dict()`
- Controlla che la serializzazione/deserializzazione preservi i dati

**Test `test_user_invalid_type`**:
- Verifica che venga sollevata un'eccezione per tipi non validi

#### Test Classe `Driver`

**Test `test_driver_creation`**:
- Verifica che un Driver abbia automaticamente `user_type = 'driver'`

#### Test Classe `Passenger`

**Test `test_passenger_creation`**:
- Verifica che un Passenger abbia automaticamente `user_type = 'passenger'`

### Test delle Feature

#### Test Registrazione

**Test `test_register_success`**:
- Simula una richiesta POST valida
- Verifica che l'utente venga creato correttamente
- Controlla la risposta JSON

**Test `test_register_missing_fields`**:
- Testa richieste con campi mancanti
- Verifica che venga restituito errore 400

**Test `test_register_short_username`**:
- Testa username troppo corti (< 3 caratteri)
- Verifica validazione

**Test `test_register_short_password`**:
- Testa password troppo corte (< 8 caratteri)
- Verifica validazione

**Test `test_register_invalid_role`**:
- Testa ruoli non validi
- Verifica che venga restituito errore 400

**Test `test_register_duplicate_username`**:
- Testa registrazione con username già esistente
- Verifica che venga restituito errore 409

**Test `test_register_driver_saves_to_drivers_json`**:
- Verifica che i driver vengano salvati in `drivers.json`

**Test `test_register_passenger_saves_to_passengers_json`**:
- Verifica che i passeggeri vengano salvati in `passengers.json`

### Esecuzione dei Test

Per eseguire tutti i test:

```bash
# Installare pytest se non già installato
pip install pytest pytest-cov

# Eseguire tutti i test
pytest

# Eseguire con coverage
pytest --cov=app tests/

# Eseguire un test specifico
pytest tests/test_models.py::test_user_creation
```

### Coverage Target

L'obiettivo è raggiungere almeno **80% di coverage** per:
- Modelli (`app/models/`)
- Route (`app/routes/`)

---

## Installazione e Configurazione

### Prerequisiti

- Python 3.8+
- Node.js 18+
- npm o yarn

### Backend

1. **Creare ambiente virtuale**:
```bash
python -m venv venv
source venv/bin/activate  # Su Windows: venv\Scripts\activate
```

2. **Installare dipendenze**:
```bash
pip install -r requirements.txt
```

3. **Configurare variabili d'ambiente** (opzionale):
```bash
# Creare file .env
echo "SECRET_KEY=your-secret-key-here" > .env
```

4. **Avviare il server**:
```bash
python app.py
```

Il server sarà disponibile su `http://localhost:5000`

### Frontend

1. **Entrare nella cartella**:
```bash
cd nuxt-app
```

2. **Installare dipendenze**:
```bash
npm install
```

3. **Configurare API URL** (opzionale):
```bash
# Creare file .env
echo "NUXT_PUBLIC_API_URL=http://localhost:5000" > .env
```

4. **Avviare il server di sviluppo**:
```bash
npm run dev
```

Il frontend sarà disponibile su `http://localhost:3000`

### Struttura File di Dati

I dati vengono salvati in:
- `drivers.json`: Lista dei conducenti registrati (formato JSONL)
- `passengers.json`: Lista dei passeggeri registrati (formato JSONL)

Ogni riga contiene un oggetto JSON con:
```json
{"username": "nome_utente", "password": "hash_password", "type": "driver|passenger"}
```

---

## Note di Sviluppo

### Prossime Feature da Implementare

1. **Autenticazione e Login**: Sistema di login con JWT
2. **Gestione Auto**: CRUD per le auto disponibili
3. **Prenotazioni**: Sistema di prenotazione viaggi
4. **Database**: Migrazione da JSON a database SQL (SQLite/PostgreSQL)
5. **Validazione avanzata**: Validazione più robusta dei dati
6. **Gestione errori**: Error handling più completo

### Best Practices Implementate

- ✅ Separazione concerns (routes, models, config)
- ✅ Application Factory pattern
- ✅ Blueprint per organizzare le route
- ✅ Hash delle password (mai in chiaro)
- ✅ Validazione lato client e server
- ✅ CORS configurato correttamente
- ✅ Type hints in Python
- ✅ TypeScript nel frontend

---

## Autori

- Coccimiglio
- Mazzotti
- Snabl

---

## Licenza

[Specificare la licenza del progetto]

