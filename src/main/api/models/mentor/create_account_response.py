from src.main.api.models.mentor.base_model import BaseModel

class CreateAccountResponse(BaseModel):
    id: int
    number: str
    balance: float

