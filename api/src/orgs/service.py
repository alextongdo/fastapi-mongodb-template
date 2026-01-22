from beanie import PydanticObjectId
from pymongo.asynchronous.client_session import AsyncClientSession

from api.core.logging import get_logger
from api.src.orgs.types import Organization

logger = get_logger(__name__)


class OrgService:

    async def create(
        self, org: Organization.Create, session: AsyncClientSession | None = None
    ) -> Organization:
        new_org = Organization(**org.model_dump())
        await new_org.insert(session=session)
        logger.info(f"CREATE org: name='{new_org.name}', id='{new_org.id}'")
        return new_org

    async def get(
        self, org_id: PydanticObjectId, session: AsyncClientSession | None = None
    ) -> Organization | None:
        org = await Organization.find_one({"_id": org_id}, session=session)
        logger.info(f"GET org: id={org_id}")
        return org

    async def update(self, session: AsyncClientSession | None = None) -> Organization:
        raise NotImplementedError("Update method not implemented.")

    async def delete(self, session: AsyncClientSession | None = None) -> Organization:
        raise NotImplementedError("Delete method not implemented.")

    async def get_by_name(
        self, org_name: str, session: AsyncClientSession | None = None
    ) -> Organization | None:
        org = await Organization.find_one({"name": org_name}, session=session)
        logger.info(f"GET org: name={org_name}")
        return org
