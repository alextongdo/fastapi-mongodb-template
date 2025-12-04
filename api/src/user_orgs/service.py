from typing import Literal

from beanie import PydanticObjectId
from pymongo.asynchronous.client_session import AsyncClientSession

from api.core.logging import get_logger
from api.src.user_orgs.types import UserOrg

logger = get_logger(__name__)


class UserOrgService:

    async def create(self, session: AsyncClientSession | None = None) -> UserOrg:
        raise NotImplementedError("Create method not implemented.")

    async def get(self, session: AsyncClientSession | None = None) -> UserOrg:
        raise NotImplementedError("Get method not implemented.")

    async def update(self, session: AsyncClientSession | None = None) -> UserOrg:
        raise NotImplementedError("Update method not implemented.")

    async def delete(self, session: AsyncClientSession | None = None) -> UserOrg:
        raise NotImplementedError("Delete method not implemented.")

    async def get_all_by_org_id(
        self,
        org_id: PydanticObjectId,
        status: Literal["pending", "approved"] | None = None,
        source: Literal["user", "org"] | None = None,
        session: AsyncClientSession | None = None,
    ) -> list[UserOrg]:
        """
        General purpose method to get all user-org memberships by org id.
        Supports filtering by status and source.
        """
        query = {"org.$id": org_id}
        if status:
            query["status"] = status
        if source:
            query["source"] = source
        user_orgs = await UserOrg.find(query, session=session).to_list()
        logger.info(
            f"GET all user_orgs: org_id={org_id}, status={status}, source={source}"
        )
        return user_orgs
