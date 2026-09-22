from pydantic import BaseModel

class PopolnenieDepositAccountRequestMidlle(BaseModel):
    accountId: int
    amount: int