"""
Test per i modelli User, Driver e Passenger.
"""

import pytest
from .user_models import User, Driver, Passenger
from werkzeug.security import check_password_hash


class TestUser:
    """Test per la classe User."""
    
    def test_user_creation(self):
        """Test creazione di un utente base."""
        user = User(
            username='testuser',
            password_hash='hashed_password',
            user_type='driver'
        )
        assert user.username == 'testuser'
        assert user.password_hash == 'hashed_password'
        assert user.user_type == 'driver'
    
    def test_user_password_hashing(self):
        """Test che le password vengano hashate correttamente."""
        password1 = 'TestPassword123'
        password2 = 'AnotherPassword456'
        
        hash1 = User.hash_password(password1)
        hash2 = User.hash_password(password2)
        
        # Gli hash dovrebbero essere diversi
        assert hash1 != hash2
        # Gli hash dovrebbero essere stringhe non vuote
        assert len(hash1) > 0
        assert len(hash2) > 0
        # Lo stesso hash non dovrebbe essere generato due volte (salt random)
        hash1_again = User.hash_password(password1)
        assert hash1 != hash1_again  # Salt diverso
    
    def test_user_check_password(self):
        """Test verifica password."""
        password = 'TestPassword123'
        password_hash = User.hash_password(password)
        
        user = User(
            username='testuser',
            password_hash=password_hash,
            user_type='driver'
        )
        
        # Password corretta
        assert user.check_password(password) is True
        # Password errata
        assert user.check_password('WrongPassword') is False
        # Password vuota
        assert user.check_password('') is False
    
    def test_user_to_dict(self):
        """Test serializzazione utente in dizionario."""
        user = User(
            username='testuser',
            password_hash='hashed_password',
            user_type='driver'
        )
        
        user_dict = user.to_dict()
        
        assert user_dict['username'] == 'testuser'
        assert user_dict['password'] == 'hashed_password'
        assert user_dict['type'] == 'driver'
    
    def test_user_from_dict(self):
        """Test deserializzazione dizionario in utente."""
        data = {
            'username': 'testuser',
            'password': 'hashed_password',
            'type': 'passenger'
        }
        
        user = User.from_dict(data)
        
        assert user.username == 'testuser'
        assert user.password_hash == 'hashed_password'
        assert user.user_type == 'passenger'
    
    def test_user_round_trip(self):
        """Test serializzazione e deserializzazione completa."""
        original = User(
            username='testuser',
            password_hash='hashed_password',
            user_type='driver'
        )
        
        # Serializza
        data = original.to_dict()
        # Deserializza
        restored = User.from_dict(data)
        
        assert restored.username == original.username
        assert restored.password_hash == original.password_hash
        assert restored.user_type == original.user_type
    
    def test_user_invalid_type(self):
        """Test che venga sollevata un'eccezione per tipo non valido."""
        with pytest.raises(ValueError, match="user_type deve essere 'driver' o 'passenger'"):
            User(
                username='testuser',
                password_hash='hashed_password',
                user_type='invalid_type'
            )


class TestDriver:
    """Test per la classe Driver."""
    
    def test_driver_creation(self):
        """Test creazione di un driver."""
        driver = Driver(
            username='driver1',
            password_hash='hashed_password'
        )
        
        assert driver.username == 'driver1'
        assert driver.password_hash == 'hashed_password'
        assert driver.user_type == 'driver'
    
    def test_driver_inherits_user_methods(self):
        """Test che Driver erediti i metodi di User."""
        password = 'DriverPassword123'
        password_hash = Driver.hash_password(password)
        
        driver = Driver(
            username='driver1',
            password_hash=password_hash
        )
        
        # Test metodi ereditati
        assert driver.check_password(password) is True
        assert driver.check_password('wrong') is False
        
        driver_dict = driver.to_dict()
        assert driver_dict['type'] == 'driver'
        
        restored = Driver.from_dict(driver_dict)
        assert restored.user_type == 'driver'


class TestPassenger:
    """Test per la classe Passenger."""
    
    def test_passenger_creation(self):
        """Test creazione di un passeggero."""
        passenger = Passenger(
            username='passenger1',
            password_hash='hashed_password'
        )
        
        assert passenger.username == 'passenger1'
        assert passenger.password_hash == 'hashed_password'
        assert passenger.user_type == 'passenger'
    
    def test_passenger_inherits_user_methods(self):
        """Test che Passenger erediti i metodi di User."""
        password = 'PassengerPassword123'
        password_hash = Passenger.hash_password(password)
        
        passenger = Passenger(
            username='passenger1',
            password_hash=password_hash
        )
        
        # Test metodi ereditati
        assert passenger.check_password(password) is True
        assert passenger.check_password('wrong') is False
        
        passenger_dict = passenger.to_dict()
        assert passenger_dict['type'] == 'passenger'
        
        restored = Passenger.from_dict(passenger_dict)
        assert restored.user_type == 'passenger'

