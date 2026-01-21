from pydantic import BaseModel


class UserResponse(BaseModel):
    id: str
    name: str
    email: str

class OrganizationResponse(BaseModel):
    id: str
    name: str