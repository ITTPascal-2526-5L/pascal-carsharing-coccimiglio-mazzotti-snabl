"""
Test per la feature di registrazione.
"""

import pytest
import json
import os
from app import create_app


@pytest.fixture
def app():
    """Crea un'istanza dell'app Flask per i test."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    return app


@pytest.fixture
def client(app):
    """Crea un client di test per l'app Flask."""
    return app.test_client()


@pytest.fixture
def cleanup_files():
    """Pulisce i file JSON dopo i test."""
    yield
    # Pulisce i file di test se esistono
    test_files = ['test_drivers.json', 'test_passengers.json']
    for file in test_files:
        if os.path.exists(file):
            os.remove(file)


class TestRegisterEndpoint:
    """Test per l'endpoint di registrazione."""
    
    def test_register_success_driver(self, client, cleanup_files):
        """Test registrazione riuscita di un driver."""
        data = {
            'username': 'newdriver',
            'password': 'TestPassword123',
            'role': 'driver'
        }
        
        response = client.post('/api/register', 
                             json=data,
                             content_type='application/json')
        
        assert response.status_code == 201
        response_data = json.loads(response.data)
        assert response_data['message'] == 'Successfully registered as driver'
        assert response_data['username'] == 'newdriver'
        
        # Verifica che il file sia stato creato
        assert os.path.exists('drivers.json')
        
        # Verifica che i dati siano stati salvati
        with open('drivers.json', 'r') as f:
            lines = [line for line in f if line.strip()]
            assert len(lines) > 0
            last_user = json.loads(lines[-1])
            assert last_user['username'] == 'newdriver'
            assert last_user['type'] == 'driver'
            assert 'password' in last_user
    
    def test_register_success_passenger(self, client, cleanup_files):
        """Test registrazione riuscita di un passeggero."""
        data = {
            'username': 'newpassenger',
            'password': 'TestPassword123',
            'role': 'passenger'
        }
        
        response = client.post('/api/register',
                             json=data,
                             content_type='application/json')
        
        assert response.status_code == 201
        response_data = json.loads(response.data)
        assert response_data['message'] == 'Successfully registered as passenger'
        assert response_data['username'] == 'newpassenger'
        
        # Verifica che il file sia stato creato
        assert os.path.exists('passengers.json')
    
    def test_register_missing_fields(self, client):
        """Test registrazione con campi mancanti."""
        # Manca password
        data = {
            'username': 'testuser',
            'role': 'driver'
        }
        
        response = client.post('/api/register',
                             json=data,
                             content_type='application/json')
        
        assert response.status_code == 400
        response_data = json.loads(response.data)
        assert 'error' in response_data
        assert 'Missing required fields' in response_data['error']
    
    def test_register_no_data(self, client):
        """Test registrazione senza dati."""
        response = client.post('/api/register',
                             json=None,
                             content_type='application/json')
        
        assert response.status_code == 400
        response_data = json.loads(response.data)
        assert 'error' in response_data
    
    def test_register_short_username(self, client):
        """Test registrazione con username troppo corto."""
        data = {
            'username': 'ab',  # Meno di 3 caratteri
            'password': 'TestPassword123',
            'role': 'driver'
        }
        
        response = client.post('/api/register',
                             json=data,
                             content_type='application/json')
        
        assert response.status_code == 400
        response_data = json.loads(response.data)
        assert 'error' in response_data
        assert 'at least 3 characters' in response_data['error']
    
    def test_register_username_with_whitespace_only(self, client):
        """Test registrazione con username contenente solo spazi (dovrebbe essere rifiutato dopo trim)."""
        data = {
            'username': '   ',  # Solo spazi, dopo trim diventa stringa vuota
            'password': 'TestPassword123',
            'role': 'driver'
        }
        
        response = client.post('/api/register',
                             json=data,
                             content_type='application/json')
        
        assert response.status_code == 400
        response_data = json.loads(response.data)
        assert 'error' in response_data
        assert 'at least 3 characters' in response_data['error']
    
    def test_register_username_with_leading_trailing_whitespace(self, client, cleanup_files):
        """Test che lo username con spazi iniziali/finali venga trimmato correttamente."""
        # Registra con username con spazi
        data1 = {
            'username': '  testuser  ',
            'password': 'TestPassword123',
            'role': 'driver'
        }
        
        response1 = client.post('/api/register',
                               json=data1,
                               content_type='application/json')
        assert response1.status_code == 201
        
        # Prova a registrare di nuovo con lo stesso username ma senza spazi
        data2 = {
            'username': 'testuser',
            'password': 'AnotherPassword456',
            'role': 'passenger'
        }
        
        response2 = client.post('/api/register',
                               json=data2,
                               content_type='application/json')
        
        # Dovrebbe fallire perché lo username trimmato è già esistente
        assert response2.status_code == 409
        response_data = json.loads(response2.data)
        assert 'error' in response_data
        assert 'already exists' in response_data['error'].lower()
    
    def test_register_short_password(self, client):
        """Test registrazione con password troppo corta."""
        data = {
            'username': 'testuser',
            'password': 'Short1',  # Meno di 8 caratteri
            'role': 'driver'
        }
        
        response = client.post('/api/register',
                             json=data,
                             content_type='application/json')
        
        assert response.status_code == 400
        response_data = json.loads(response.data)
        assert 'error' in response_data
        assert 'at least 8 characters' in response_data['error']
    
    def test_register_invalid_role(self, client):
        """Test registrazione con ruolo non valido."""
        data = {
            'username': 'testuser',
            'password': 'TestPassword123',
            'role': 'invalid_role'
        }
        
        response = client.post('/api/register',
                             json=data,
                             content_type='application/json')
        
        assert response.status_code == 400
        response_data = json.loads(response.data)
        assert 'error' in response_data
        assert 'Invalid role' in response_data['error']
    
    def test_register_duplicate_username(self, client, cleanup_files):
        """Test registrazione con username già esistente."""
        # Prima registrazione
        data1 = {
            'username': 'duplicateuser',
            'password': 'TestPassword123',
            'role': 'driver'
        }
        
        response1 = client.post('/api/register',
                               json=data1,
                               content_type='application/json')
        assert response1.status_code == 201
        
        # Seconda registrazione con stesso username
        data2 = {
            'username': 'duplicateuser',
            'password': 'AnotherPassword456',
            'role': 'passenger'
        }
        
        response2 = client.post('/api/register',
                               json=data2,
                               content_type='application/json')
        
        assert response2.status_code == 409
        response_data = json.loads(response2.data)
        assert 'error' in response_data
        assert 'already exists' in response_data['error'].lower()
    
    def test_register_driver_saves_to_drivers_json(self, client, cleanup_files):
        """Test che i driver vengano salvati in drivers.json."""
        data = {
            'username': 'driver_test',
            'password': 'TestPassword123',
            'role': 'driver'
        }
        
        client.post('/api/register',
                   json=data,
                   content_type='application/json')
        
        assert os.path.exists('drivers.json')
        
        with open('drivers.json', 'r') as f:
            users = []
            for line in f:
                if line.strip():
                    users.append(json.loads(line))
        
        # Verifica che ci sia almeno un driver
        driver_users = [u for u in users if u.get('type') == 'driver']
        assert len(driver_users) > 0
    
    def test_register_passenger_saves_to_passengers_json(self, client, cleanup_files):
        """Test che i passeggeri vengano salvati in passengers.json."""
        data = {
            'username': 'passenger_test',
            'password': 'TestPassword123',
            'role': 'passenger'
        }
        
        client.post('/api/register',
                   json=data,
                   content_type='application/json')
        
        assert os.path.exists('passengers.json')
        
        with open('passengers.json', 'r') as f:
            users = []
            for line in f:
                if line.strip():
                    users.append(json.loads(line))
        
        # Verifica che ci sia almeno un passeggero
        passenger_users = [u for u in users if u.get('type') == 'passenger']
        assert len(passenger_users) > 0
    
    def test_register_password_is_hashed(self, client, cleanup_files):
        """Test che la password venga hashata e non salvata in chiaro."""
        data = {
            'username': 'hashtest',
            'password': 'PlainPassword123',
            'role': 'driver'
        }
        
        client.post('/api/register',
                   json=data,
                   content_type='application/json')
        
        # Legge il file e verifica che la password sia hashata
        with open('drivers.json', 'r') as f:
            for line in f:
                if line.strip():
                    user = json.loads(line)
                    if user['username'] == 'hashtest':
                        # La password hashata non dovrebbe essere uguale a quella in chiaro
                        assert user['password'] != 'PlainPassword123'
                        # La password hashata dovrebbe iniziare con 'scrypt:' (algoritmo usato da werkzeug)
                        assert user['password'].startswith('scrypt:')
                        break

