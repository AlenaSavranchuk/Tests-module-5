from pydantic import BaseModel


class TransferRequestMiddle(BaseModel):
    fromAccountId: int
    toAccountId: int
    amount: float