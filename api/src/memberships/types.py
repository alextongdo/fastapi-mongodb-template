from typing import Literal

from beanie import Document, Link, PydanticObjectId
from pydantic import BaseModel, Field
from pymongo import IndexModel

from api.src.orgs.types import Organization
from api.src.users.types import User


class Membership(Document):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId, alias="_id")
    org: Link[Organization]
    user: Link[User]
    status: Literal["pending", "approved"] = "pending"
    source: Literal["user", "org"]

    class Settings:
        name = "memberships"
        indexes = [
            IndexModel(
                [("org", 1), ("user", 1)],
                unique=True,
            )
        ]

    class Response(BaseModel):
        id: PydanticObjectId
        org: Organization.Response
        user: User.Response
        status: Literal["pending", "approved"]
        source: Literal["user", "org"]

    class ListResponse(BaseModel):
        memberships: list["Membership.Response"]

    class Request(BaseModel):
        org_id: str

    class Invite(BaseModel):
        org_id: str
        user_id: PydanticObjectId

    class Create(BaseModel):
        org_id: PydanticObjectId
        user_id: PydanticObjectId
        source: Literal["user", "org"]
