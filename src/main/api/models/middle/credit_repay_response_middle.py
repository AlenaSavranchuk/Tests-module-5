from pydantic import BaseModel

class CreditRepayResponseMiddle(BaseModel):
    creditId: int
    amountDeposited: int