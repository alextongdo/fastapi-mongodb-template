from typing import Literal

from beanie import Document, Link, PydanticObjectId
from pydantic import BaseModel, Field

from api.src.orgs.types import Organization
from api.src.users.types import User


class UserOrg(Document):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId, alias="_id")
    org: Link[Organization]
    user: Link[User]
    status: Literal["pending", "approved"] = "pending"
    source: Literal["user", "org"]

    class Settings:
        name = "user_orgs"

    class Response(BaseModel):
        id: PydanticObjectId
        org: Organization.Response
        user: User.Response
        status: Literal["pending", "approved"]
