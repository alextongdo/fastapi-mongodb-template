from typing import Literal

from beanie import PydanticObjectId
from pymongo.asynchronous.client_session import AsyncClientSession

from api.core.logging import get_logger
from api.src.memberships.types import Membership

logger = get_logger(__name__)


class MembershipService:

    async def create(
        self, membership: Membership.Create, session: AsyncClientSession | None = None
    ) -> Membership:
        mbrship = Membership(
            org=membership.org_id,
            user=membership.user_id,
            source=membership.source,
        )
        await mbrship.create(session=session)
        logger.info(
            "CREATE membership: "
            f"org_id={mbrship.org.ref.id}, user_id={mbrship.user.ref.id}"
        )
        return mbrship

    async def get(self, session: AsyncClientSession | None = None) -> Membership:
        raise NotImplementedError("Get method not implemented.")

    async def update(self, session: AsyncClientSession | None = None) -> Membership:
        raise NotImplementedError("Update method not implemented.")

    async def delete(self, session: AsyncClientSession | None = None) -> Membership:
        raise NotImplementedError("Delete method not implemented.")

    async def get_all_by_org_id(
        self,
        org_id: PydanticObjectId,
        status: Literal["pending", "approved"] | None = None,
        source: Literal["user", "org"] | None = None,
        session: AsyncClientSession | None = None,
    ) -> list[Membership]:
        """
        General purpose method to get all memberships by org id.
        Supports filtering by status and source.
        """
        query = {"org.$id": org_id}
        if status:
            query["status"] = status
        if source:
            query["source"] = source
        memberships = await Membership.find(query, session=session).to_list()
        logger.info(
            f"GET all memberships: org_id={org_id}, status={status}, source={source}"
        )
        return memberships

    async def get_all_by_user_id(
        self,
        user_id: PydanticObjectId,
        status: Literal["pending", "approved"] | None = None,
        source: Literal["user", "org"] | None = None,
        session: AsyncClientSession | None = None,
    ) -> list[Membership]:
        """
        General purpose method to get all memberships by user id.
        Supports filtering by status and source.
        """
        query = {"user.$id": user_id}
        if status:
            query["status"] = status
        if source:
            query["source"] = source
        memberships = await Membership.find(query, session=session).to_list()
        logger.info(
            f"GET all memberships: user_id={user_id}, status={status}, source={source}"
        )
        return memberships

    async def get_by_org_and_user_id(
        self,
        org_id: PydanticObjectId,
        user_id: PydanticObjectId,
        session: AsyncClientSession | None = None,
    ) -> Membership | None:
        """
        Get a membership by org id and user id.
        """
        membership = await Membership.find_one(
            {"org.$id": org_id, "user.$id": user_id}, session=session
        )
        logger.info(f"GET membership: org_id={org_id}, user_id={user_id}")
        return membership
