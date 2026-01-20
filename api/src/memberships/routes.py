from beanie import PydanticObjectId
from fastapi import APIRouter, Depends

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
    # check if user is in organization to be inviting others
    # create pending membership
    pass


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
