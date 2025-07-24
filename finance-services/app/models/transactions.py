from sqlalchemy import Column, Integer, Float, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.utils.database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    bank_id = Column(Integer, ForeignKey("banks.id", ondelete="CASCADE"))
    amount = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime.now(timezone.utc))
    type = Column(String(50))
    category = Column(String(50))
    pending = Column(Boolean, default=False)
    sender_bank_id = Column(Integer, nullable=True)
    receiver_bank_id = Column(Integer, nullable=True)

    user = relationship("User")
    bank = relationship("Bank")