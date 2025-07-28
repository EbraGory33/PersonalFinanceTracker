from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.utils.database import Base

class Bank(Base):
    __tablename__ = "banks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    bank_id = Column(String(100))  # Plaid bank ID
    account_id = Column(String(100))
    access_token = Column(String)  # Store encrypted in logic
    funding_source_url = Column(String(255))
    sharable_id = Column(String(100))

    user = relationship("User", back_populates="banks")
    transactions = relationship(
        "Transaction",
        back_populates="bank",
        cascade="all, delete-orphan"
    )