# Test Suite - Pascal Car Sharing

## Panoramica

Questa directory contiene tutti i test per il progetto Pascal Car Sharing. I test sono organizzati per moduli e feature.

## Struttura

```
tests/
├── __init__.py              # Inizializzazione del modulo test
├── conftest.py              # Configurazione pytest e fixtures
├── test_models.py           # Test per i modelli (User, Driver, Passenger)
├── test_register.py         # Test per la feature di registrazione
└── README.md                # Questo file
```

## Dipendenze

I test richiedono:
- `pytest>=8.3.4`
- `pytest-cov>=6.0.0` (per il coverage)

Installare con:
```bash
pip install -r requirements.txt
```

## Esecuzione dei Test

### Eseguire tutti i test

```bash
pytest
```

### Eseguire con output verboso

```bash
pytest -v
```

### Eseguire con coverage

```bash
pytest --cov=app --cov-report=html
```

Questo genererà un report HTML in `htmlcov/index.html`.

### Eseguire un file specifico

```bash
pytest tests/test_models.py
```

### Eseguire un test specifico

```bash
pytest tests/test_models.py::TestUser::test_user_creation
```

## Test Disponibili

### test_models.py

Test per i modelli di dati:

- **TestUser**:
  - `test_user_creation`: Verifica creazione utente
  - `test_user_password_hashing`: Verifica hashing password
  - `test_user_check_password`: Verifica verifica password
  - `test_user_to_dict`: Verifica serializzazione
  - `test_user_from_dict`: Verifica deserializzazione
  - `test_user_round_trip`: Verifica ciclo completo serializzazione/deserializzazione
  - `test_user_invalid_type`: Verifica validazione tipo

- **TestDriver**:
  - `test_driver_creation`: Verifica creazione driver
  - `test_driver_inherits_user_methods`: Verifica ereditarietà

- **TestPassenger**:
  - `test_passenger_creation`: Verifica creazione passeggero
  - `test_passenger_inherits_user_methods`: Verifica ereditarietà

### test_register.py

Test per l'endpoint di registrazione:

- `test_register_success_driver`: Registrazione driver riuscita
- `test_register_success_passenger`: Registrazione passeggero riuscita
- `test_register_missing_fields`: Campi mancanti
- `test_register_no_data`: Nessun dato fornito
- `test_register_short_username`: Username troppo corto
- `test_register_short_password`: Password troppo corta
- `test_register_invalid_role`: Ruolo non valido
- `test_register_duplicate_username`: Username duplicato
- `test_register_driver_saves_to_drivers_json`: Salvataggio driver
- `test_register_passenger_saves_to_passengers_json`: Salvataggio passeggero
- `test_register_password_is_hashed`: Verifica hashing password

## Fixtures

Le fixtures disponibili in `conftest.py`:

- `app`: Istanza dell'app Flask per i test
- `client`: Client di test per fare richieste HTTP
- `temp_drivers_file`: File temporaneo per i driver
- `temp_passengers_file`: File temporaneo per i passeggeri
- `sample_user_data`: Dati di esempio per un utente
- `existing_driver_data`: Dati di un driver esistente

## Coverage Target

L'obiettivo è mantenere almeno **80% di coverage** per:
- `app/models/`
- `app/routes/`

Verificare il coverage con:
```bash
pytest --cov=app --cov-report=term-missing
```

## Best Practices

1. **Isolamento**: Ogni test è indipendente e non dipende da altri test
2. **Cleanup**: I file di test vengono puliti automaticamente dopo l'esecuzione
3. **Naming**: I nomi dei test descrivono chiaramente cosa testano
4. **AAA Pattern**: Arrange, Act, Assert in ogni test
5. **Fixtures**: Utilizzo di fixtures per setup/teardown comune

## Aggiungere Nuovi Test

Quando si aggiunge una nuova feature:

1. Creare un nuovo file `test_<feature>.py`
2. Importare le fixtures necessarie da `conftest.py`
3. Seguire il pattern AAA (Arrange, Act, Assert)
4. Aggiungere test per:
   - Casi di successo
   - Casi di errore
   - Validazione input
   - Edge cases

Esempio:

```python
def test_new_feature_success(client):
    """Test che la nuova feature funzioni correttamente."""
    # Arrange
    data = {'key': 'value'}
    
    # Act
    response = client.post('/api/new-endpoint', json=data)
    
    # Assert
    assert response.status_code == 200
    assert 'expected_key' in response.json
```

