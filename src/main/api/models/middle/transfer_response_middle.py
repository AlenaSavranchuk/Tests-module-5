from pydantic import BaseModel


class TransferResponseMiddle(BaseModel):
    fromAccountId: int
    toAccountId: int
    fromAccountIdBalance: float