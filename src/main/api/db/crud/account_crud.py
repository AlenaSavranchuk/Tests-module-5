from sqlalchemy.orm import Session
from src.main.api.db.models.account_table import Account
from src.main.api.db.models.user_table import User

class AccountCrudDb:
    @staticmethod
    def get_account_by_id(db: Session, account_id: int) -> Account | None:
        return db.query(Account).filter_by(id=account_id).first()

    @staticmethod
    def delete_account(db: Session, account_id: int) -> None:
        account = db.query(Account).filter_by(id=account_id).first()
        if account:
            db.delete(account)
            db.commit()

    @staticmethod
    def get_account_balance(db: Session, account_id:int) -> int:
        return db.query(Account.balance).filter_by(id=account_id).scalar()

    @staticmethod
    def popolnenie_balance(db: Session, account_id: int, amount: float) -> Account:
        account = db.query(Account).filter_by(id=account_id).scalar()
        account.balance = amount
        db.commit()
        return account

