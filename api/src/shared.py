from beanie import PydanticObjectId
from pydantic import BaseModel


class UserResponse(BaseModel):
    id: PydanticObjectId
    name: str
    email: str

class OrganizationResponse(BaseModel):
    id: PydanticObjectId
    name: str