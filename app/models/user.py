"""
Modelli per la gestione degli utenti del sistema di car sharing.
"""

from dataclasses import dataclass
from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash


@dataclass
class User:
    """
    Classe base per rappresentare un utente del sistema.
    
    Attributi:
        username (str): Nome utente univoco
        password_hash (str): Hash della password
        user_type (str): Tipo di utente ('driver' o 'passenger')
    """
    username: str
    password_hash: str
    user_type: Optional[str] = None
    
    def __post_init__(self):
        """Valida il tipo di utente dopo l'inizializzazione."""
        # Validate only if a user_type was provided. Subclasses (Driver/Passenger)
        # will set the proper type in their own __post_init__.
        if self.user_type is not None and self.user_type not in ['driver', 'passenger']:
            raise ValueError("user_type deve essere 'driver' o 'passenger'")
    
    def check_password(self, password: str) -> bool:
        """
        Verifica se la password fornita corrisponde all'hash salvato.
        
        Args:
            password (str): Password in chiaro da verificare
            
        Returns:
            bool: True se la password è corretta, False altrimenti
        """
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self) -> dict:
        """
        Converte l'utente in un dizionario.
        
        Returns:
            dict: Dizionario con i dati dell'utente
        """
        return {
            'username': self.username,
            'password': self.password_hash,
            'type': self.user_type
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        """
        Crea un'istanza di User da un dizionario.
        
        Args:
            data (dict): Dizionario con i dati dell'utente
            
        Returns:
            User: Istanza di User
        """
        return cls(
            username=data.get('username'),
            password_hash=data.get('password'),
            user_type=data.get('type')
        )
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Genera l'hash di una password.
        
        Args:
            password (str): Password in chiaro
            
        Returns:
            str: Hash della password
        """
        return generate_password_hash(password)


@dataclass
class Driver(User):
    """
    Classe per rappresentare un conducente.
    Eredita da User e imposta automaticamente il tipo a 'driver'.
    """
    def __post_init__(self):
        """Imposta il tipo di utente come driver."""
        self.user_type = 'driver'
        super().__post_init__()


@dataclass
class Passenger(User):
    """
    Classe per rappresentare un passeggero.
    Eredita da User e imposta automaticamente il tipo a 'passenger'.
    """
    def __post_init__(self):
        """Imposta il tipo di utente come passenger."""
        self.user_type = 'passenger'
        super().__post_init__()

