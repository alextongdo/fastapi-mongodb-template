from typing import Annotated

from beanie import Document, Indexed, PydanticObjectId
from pydantic import BaseModel, Field


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

    class Response(BaseModel):
        id: PydanticObjectId
        auth0_id: str
        name: str
        email: str
        orgs: list["OrgReponse"] = Field(default_factory=list)

        class OrgReponse(BaseModel):
            id: PydanticObjectId
            name: str
