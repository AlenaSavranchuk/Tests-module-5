from pydantic import BaseModel

class CreditRepayRequestMiddle(BaseModel):
    creditId: int
    accountId: int
    amount: int
