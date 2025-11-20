"""
Configurazione pytest per i test.
"""

import pytest
import os
import json
import tempfile
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
def temp_drivers_file():
    """Crea un file temporaneo per i driver."""
    fd, path = tempfile.mkstemp(suffix='.json')
    yield path
    os.close(fd)
    if os.path.exists(path):
        os.remove(path)


@pytest.fixture
def temp_passengers_file():
    """Crea un file temporaneo per i passeggeri."""
    fd, path = tempfile.mkstemp(suffix='.json')
    yield path
    os.close(fd)
    if os.path.exists(path):
        os.remove(path)


@pytest.fixture
def sample_user_data():
    """Dati di esempio per un utente."""
    return {
        'username': 'testuser',
        'password': 'TestPassword123',
        'role': 'driver'
    }


@pytest.fixture
def existing_driver_data():
    """Dati di un driver esistente per test di duplicati."""
    return {
        'username': 'existingdriver',
        'password': 'scrypt:32768:8:1$hash$hash',
        'type': 'driver'
    }

