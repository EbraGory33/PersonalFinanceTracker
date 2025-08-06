from sqlalchemy import Column, Integer, Float, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.utils.database import Base


#  TODO: refine the model: add email field later
class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    sender_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    receiver_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    sender_bank_id = Column(Integer, ForeignKey("banks.id", ondelete="CASCADE"))
    receiver_bank_id = Column(Integer, ForeignKey("banks.id", ondelete="CASCADE"))
    amount = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime.now(timezone.utc))
    type = Column(String(50))
    category = Column(String(50))
    channel = Column(String(50))
    pending = Column(Boolean, default=True)

    sender = relationship(
        "User", foreign_keys=[sender_id], back_populates="sent_transactions"
    )
    receiver = relationship(
        "User", foreign_keys=[receiver_id], back_populates="received_transactions"
    )
    sender_bank = relationship(
        "Bank", foreign_keys=[sender_bank_id], back_populates="sent_transactions"
    )
    receiver_bank = relationship(
        "Bank", foreign_keys=[receiver_bank_id], back_populates="received_transactions"
    )
