from typing import Annotated

from beanie import Document, Indexed, PydanticObjectId
from pydantic import BaseModel, Field, StringConstraints

from api.src.shared import OrganizationResponse, UserResponse


class Organization(Document):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId, alias="_id")
    name: Annotated[str, Indexed(unique=True)]

    class Settings:
        name = "orgs"

    class Create(BaseModel):
        name: Annotated[
            str,
            # Must contain only letters, _, or - and length between 8 and 100 characters
            StringConstraints(
                strip_whitespace=True,
                min_length=5,
                max_length=100,
                pattern=r"^[a-zA-Z-_]+$",
            ),
        ]

    class Response(OrganizationResponse):
        pass

    class DetailResponse(BaseModel):
        id: PydanticObjectId
        name: str
        users: list[UserResponse] = Field(default_factory=list)
