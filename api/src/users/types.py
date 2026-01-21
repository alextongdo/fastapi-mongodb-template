from typing import Annotated

from beanie import Document, Indexed, PydanticObjectId
from pydantic import BaseModel, Field

from api.src.shared import OrganizationResponse, UserResponse


class User(Document):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId, alias="_id")
    auth0_id: Annotated[str, Indexed(unique=True)]
    name: str
    email: str

    class Settings:
        name = "users"

    class Update(BaseModel):
        name: str
        email: str

    class Response(UserResponse):
        pass

    class DetailResponse(BaseModel):
        id: PydanticObjectId
        auth0_id: str
        name: str
        email: str
        orgs: list[OrganizationResponse] = Field(default_factory=list)
