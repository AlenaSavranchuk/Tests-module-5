from sqlalchemy import Column, Integer, DateTime, Float
from src.main.api.db.base import Base


class Credit(Base):
    __tablename__ = 'credit'
    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, unique=True)
    amount = Column(Float)
    term_months = Column(Integer)
    balance = Column(Float)
    created_at = Column(DateTime)

    def __repr__(self):
        return f'<Credit(id={self.id}, account_id={self.account_id},amount={self.amount},term_months={self.term_months},balance={self.balance},created_at={self.created_at})>'