from fastapi import APIRouter, Depends

from api.src.auth.auth0 import get_authed_user
from api.src.memberships.service import MembershipService
from api.src.users.types import User

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=User.DetailResponse)
async def get_user(
    user: User = Depends(get_authed_user),
    membership_service: MembershipService = Depends(MembershipService),
):
    """Return the authenticated user's profile and approved org memberships."""
    memberships = await membership_service.get_all_by_user_id(
        user_id=user.id, status="approved"
    )

    for membership in memberships:
        await membership.fetch_link("org")

    return {
        "id": user.id,
        "auth0_id": user.auth0_id,
        "name": user.name,
        "email": user.email,
        "orgs": [
            {
                "id": membership.org.id,
                "name": membership.org.name,
            }
            for membership in memberships
        ],
    }
