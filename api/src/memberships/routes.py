from beanie import PydanticObjectId
from fastapi import APIRouter, Depends

from api.core.exceptions import ValidationException
from api.src.auth.auth0 import get_authed_user
from api.src.memberships.service import MembershipService
from api.src.memberships.types import Membership
from api.src.users.types import User

router = APIRouter(prefix="/memberships", tags=["memberships"])


@router.post("/invites", response_model=Membership.Response)
async def invite_user_to_org(
    payload: Membership.Invite,
    user: User = Depends(get_authed_user),
    membership_service: MembershipService = Depends(MembershipService),
):
    """Members of an organization can invite a user to join the org."""
    if payload.user_id == user.id:
        raise ValidationException("Cannot invite yourself to an organization.")
    # check if user is in organization to be inviting others
    if not await membership_service.get_by_org_and_user_id(
        org_id=payload.org_id,
        user_id=user.id,
    ):
        raise ValidationException("You are not a member of this organization.")
    # create pending membership
    membership = await membership_service.create(
        Membership.Create(
            org_id=payload.org_id,
            user_id=payload.user_id,
            source="org",
        )
    )
    await membership.fetch_link("org")
    await membership.fetch_link("user")
    return {
        "id": membership.id,
        "org": {
            "id": membership.org.id,
            "name": membership.org.name,
        },
        "user": {
            "id": membership.user.id,
            "name": membership.user.name,
            "email": membership.user.email,
        },
        "status": membership.status,
        "source": membership.source,
    }


@router.post("/requests", response_model=Membership.Response)
async def request_to_join_org(
    payload: Membership.Request,
    user: User = Depends(get_authed_user),
):
    """A user can request to join an organization."""
    # get org to check if it exists
    # create pending membership
    pass


@router.get("/pending", response_model=Membership.ListResponse)
async def get_all_pending_memberships(
    user: User = Depends(get_authed_user),
    membership_service: MembershipService = Depends(MembershipService),
):
    """
    Get all pending membership requests including both invites and requests
    for the user.
    """
    # get all pending memberships for a user
    pass


@router.delete("/invites/{membership_id}", response_model=Membership.Response)
async def cancel_invite(
    membership_id: PydanticObjectId,
    user: User = Depends(get_authed_user),
    membership_service: MembershipService = Depends(MembershipService),
):
    """Cancel a membership invite."""
    # check if user is in organization to be cancelling invite
    # delete membership
    pass


@router.delete("/requests/{membership_id}", response_model=Membership.Response)
async def cancel_request(
    membership_id: PydanticObjectId,
    user: User = Depends(get_authed_user),
    membership_service: MembershipService = Depends(MembershipService),
):
    """Cancel a membership request."""
    # delete membership
    pass
