from pydantic import BaseModel
from pydantic import Field, AliasChoices

class CreditRequestMiddle(BaseModel):
    accountId: int = Field(validation_alias=AliasChoices('id', 'accountId'))
    amount: int
    termMonths: int
