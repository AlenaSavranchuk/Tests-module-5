from pydantic import BaseModel

class DeleteUserRequestMiddle(BaseModel):
    id: int