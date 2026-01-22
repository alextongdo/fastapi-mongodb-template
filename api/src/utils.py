from beanie import PydanticObjectId

from api.src.memberships.types import Membership
from api.src.orgs.types import Organization
from api.src.users.types import User


def num_to_object_id(num: int) -> PydanticObjectId:
    assert 0 <= num < 10**24
    return PydanticObjectId(f"{num:024d}")


async def seed_db():
    await seed_users()
    await seed_orgs()
    await seed_user_orgs()


async def seed_users():
    users = [
        User(
            id=num_to_object_id(1),
            auth0_id="fake_auth0_id",
            name="Fake Auth0 User",
            email="fake@auth0.com",
        )
    ]
    await User.insert_many(users)


async def seed_orgs():
    orgs = [Organization(id=num_to_object_id(2), name="fake-org")]
    await Organization.insert_many(orgs)


async def seed_user_orgs():
    user_orgs = [
        Membership(
            org=num_to_object_id(2),
            user=num_to_object_id(1),
            status="approved",
        )
    ]
    await Membership.insert_many(user_orgs)
