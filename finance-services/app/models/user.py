from sqlalchemy import Column, Integer, String, Boolean
from app.utils.database import Base


class User(Base):
    """
    SQLAlchemy ORM model representing a user in the system.

    Attributes:
        id (int): Primary key.
        first_name (str): User's first name.
        last_name (str): User's last name.
        email (str): Unique user email address.
        hashed_password (str): Hashed password for authentication.
        address1 (str): Primary address line.
        city (str): City of residence.
        state (str): State of residence.
        postal_code (str): Postal/ZIP code.
        date_of_birth (str): Date of birth, stored as string (format YYYY-MM-DD).
        ssn (str): Encrypted Social Security Number (optional).
        dwolla_customer_id (str): Customer ID from Dwolla (optional).
        dwolla_customer_url (str): Customer URL from Dwolla (optional).
        is_active (bool): User account active status.
    """
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    address1 = Column(String(255))
    city = Column(String(50))
    state = Column(String(50))
    postal_code = Column(String(10))
    date_of_birth = Column(String(10))  # Store as string or DATE type
    ssn = Column(String, nullable=True)  # Encrypt this in logic layer
    dwolla_customer_id = Column(String(100), nullable=True)
    dwolla_customer_url = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
