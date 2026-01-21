
import pymongo
from pymongo.asynchronous.client_session import AsyncClientSession

from api.core.logging import get_logger
from api.src.users.types import User

logger = get_logger(__name__)


class UserService:

    async def create(self, session: AsyncClientSession | None = None) -> User:
        raise NotImplementedError("Create method not implemented.")

    async def get(self, session: AsyncClientSession | None = None) -> User:
        raise NotImplementedError("Get method not implemented.")

    async def update(self, session: AsyncClientSession | None = None) -> User:
        raise NotImplementedError("Update method not implemented.")

    async def delete(self, session: AsyncClientSession | None = None) -> User:
        raise NotImplementedError("Delete method not implemented.")

    async def get_by_auth0_id(
        self, auth0_id: str, session: AsyncClientSession | None = None
    ) -> User | None:
        user = await User.find_one({"auth0_id": auth0_id}, session=session)
        logger.info(f"GET user: auth0_id={auth0_id}")
        return user

    async def upsert_by_auth0_id(
        self,
        auth0_id: str,
        user_update: User.Update,
        session: AsyncClientSession | None = None,
    ) -> User:
        """
        Atomic operation to either find a user by auth0
        id and update them, or create a new one.
        """
        result = await User.find_one(User.auth0_id == auth0_id).update(
            {"$set": user_update.model_dump() | {"auth0_id": auth0_id}},
            upsert=True,
            response_type=pymongo.ReturnDocument.AFTER,
            session=session,
        )
        logger.info(f"UPSERT user: auth0_id={auth0_id}")
        return result
