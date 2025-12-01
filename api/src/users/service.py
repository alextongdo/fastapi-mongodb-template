from typing import Optional
import pymongo
from pymongo.asynchronous.client_session import AsyncClientSession


from api.core.exceptions import NotFoundException
from api.core.logging import get_logger
from api.src.users.types import User


logger = get_logger(__name__)


class UserService:

    async def create(self, session: Optional[AsyncClientSession] = None) -> User:
        raise NotImplementedError("Create method not implemented.")

    async def get(self, session: Optional[AsyncClientSession] = None) -> User:
        raise NotImplementedError("Get method not implemented.")

    async def update(self, session: Optional[AsyncClientSession] = None) -> User:
        raise NotImplementedError("Update method not implemented.")

    async def delete(self, session: Optional[AsyncClientSession] = None) -> User:
        raise NotImplementedError("Delete method not implemented.")

    async def get_by_auth0_id(
        self, auth0_id: str, session: Optional[AsyncClientSession] = None
    ) -> User:
        user = await User.find_one({"auth0_id": auth0_id}, session=session)
        if not user:
            raise NotFoundException(f"User with auth0_id '{auth0_id}' not found")

        logger.info(f"Retrieved user with auth0_id: {auth0_id}")
        return user

    async def upsert_by_auth0_id(
        self,
        auth0_id: str,
        user_update: User.Update,
        session: Optional[AsyncClientSession] = None,
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
        logger.info(f"Upserted user with auth0_id: {auth0_id}")
        return result
