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
        )
        await mbrship.create(session=session)
        logger.info(
            "CREATE membership: "
            f"org_id={mbrship.org.ref.id}, user_id={mbrship.user.ref.id}"
        )
        return mbrship

    async def get(
        self,
        membership_id: PydanticObjectId | None = None,
        org_id: PydanticObjectId | None = None,
        user_id: PydanticObjectId | None = None,
        session: AsyncClientSession | None = None,
    ) -> Membership | None:
        """
        Get a membership by either membership_id or (org_id, user_id).
        """
        if membership_id is not None:
            filter = {"_id": membership_id}
        elif org_id is not None and user_id is not None:
            filter = {"org.$id": org_id, "user.$id": user_id}
        else:
            raise ValueError(
                "Must provide either membership_id or both org_id and user_id"
            )

        membership = await Membership.find_one(filter, session=session)
        logger.info(
            "GET membership: "
            f"membership_id={membership_id}, org_id={org_id}, user_id={user_id}"
        )
        return membership

    async def update(
        self, payload: Membership.Update, session: AsyncClientSession | None = None
    ) -> Membership | None:
        membership = await self.get(payload.id, session=session)
        if not membership:
            return None
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(membership, field, value)
        await membership.save(session=session)
        logger.info(f"UPDATE membership: id={membership.id}")
        return membership

    async def delete(
        self, membership_id: PydanticObjectId, session: AsyncClientSession | None = None
    ) -> Membership | None:
        membership = await self.get(membership_id=membership_id, session=session)
        if not membership:
            return None
        await membership.delete(session=session)
        logger.info(f"DELETE membership: id={membership.id}")
        return membership

    async def get_all(
        self,
        org_id: PydanticObjectId | None = None,
        user_id: PydanticObjectId | None = None,
        status: Literal["pending", "approved"] | None = None,
        fetch_links: bool = False,
        session: AsyncClientSession | None = None,
    ) -> list[Membership]:
        """
        General purpose method to get all memberships.
        Supports optional filtering by org, user, and status.
        """
        query = {}
        if org_id:
            query["org.$id"] = org_id
        if user_id:
            query["user.$id"] = user_id
        if status:
            query["status"] = status
        memberships = await Membership.find(
            query, fetch_links=fetch_links, session=session
        ).to_list()
        logger.info(
            f"GET all memberships: org_id={org_id}, user_id={user_id}, status={status}"
        )
        return memberships
