from sqlalchemy.orm import Session
from src.main.api.db.models.credit_table import Credit

class CreditCrudDb:
    @staticmethod
    # фильтр по айди кредита
    def get_credit_id(db: Session, id: int) -> Credit | None:
        return db.query(Credit).filter_by(id=id).first()

    @staticmethod
    # фильтр по сумме кредитов?
    def get_credit_count(db: Session, account_id: int)-> int:
        return db.query(Credit).filter_by(account_id=account_id).count()

