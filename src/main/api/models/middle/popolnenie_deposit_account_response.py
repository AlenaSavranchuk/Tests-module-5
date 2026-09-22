from pydantic import BaseModel

class PopolnenieDepositAccountResponseMiddle(BaseModel):
    id: int
    balance: float