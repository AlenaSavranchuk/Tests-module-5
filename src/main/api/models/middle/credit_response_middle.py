from pydantic import BaseModel
from pydantic import Field, AliasChoices

class CreditResponseMiddle(BaseModel):
    accountId: int = Field(validation_alias=AliasChoices('id', 'accountId'))
    amount: int
    termMonths: int
    balance: int
    creditId: int
