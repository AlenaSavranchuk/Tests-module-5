from pydantic import BaseModel

class LoginUserResponseMiddle(BaseModel):
     token: str

