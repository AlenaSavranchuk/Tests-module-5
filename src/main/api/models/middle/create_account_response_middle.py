from pydantic import BaseModel

class CreateAccountResponseMiddle(BaseModel):
    id: int
    number: str
    balance: float
