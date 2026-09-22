from sqlalchemy.orm import Session
from src.main.api.db.models.transaction_table import Transaction

class TransactionCrud:
    @staticmethod
    def get_transaction_id(db: Session, to_account_id: int) -> Transaction | None:
        return db.query(Transaction).filter_by(to_account_id=to_account_id).first()

    @staticmethod
    def get_transaction_amount(db: Session, amount: float) -> Transaction | None:
        return db.query(Transaction).filter_by(amount=amount).first()

    def get_transaction_account(db: Session, from_account_id: int, to_account_id: int) -> Transaction | None:
        return db.query(Transaction).filter_by(from_account_id=from_account_id, to_account_id=to_account_id).first()
