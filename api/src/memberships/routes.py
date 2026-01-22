from beanie import PydanticObjectId
from fastapi import APIRouter, Depends

from api.core.exceptions import NotFoundException, ValidationException
from api.src.auth.auth0 import get_authed_user
from api.src.memberships.service import MembershipService
from api.src.memberships.types import Membership
from api.src.orgs.types import Organization
from api.src.users.types import User

router = APIRouter(prefix="/memberships", tags=["memberships"])


@router.post("/invites")
async def invite_user_to_org(
    payload: Membership.Create,
    user: User = Depends(get_authed_user),
    membership_service: MembershipService = Depends(MembershipService),
) -> Membership.Response:
    """Members of an organization can invite a user to join the org."""
    if payload.user_id == user.id:
        raise ValidationException("Cannot invite yourself to an organization.")
    # check if user is in organization to be inviting others
    if not await membership_service.get(
        org_id=payload.org_id,
        user_id=user.id,
    ):
        raise ValidationException("You are not a member of this organization.")
    # create pending membership
    membership = await membership_service.create(
        Membership.Create(
            org_id=payload.org_id,
            user_id=payload.user_id,
        )
    )
    await membership.fetch_link("org")
    await membership.fetch_link("user")
    return Membership.Response(
        id=membership.id,
        org=Organization.Response(
            id=membership.org.id,
            name=membership.org.name,
        ),
        user=User.Response(
            id=membership.user.id,
            name=membership.user.name,
            email=membership.user.email,
        ),
        status=membership.status,
    )


@router.get("/invites/pending")
async def get_all_pending_memberships(
    user: User = Depends(get_authed_user),
    membership_service: MembershipService = Depends(MembershipService),
) -> Membership.ListResponse:
    """
    Get all pending membership invites for the user.
    """
    memberships = await membership_service.get_all(
        user_id=user.id,
        status="pending",
        fetch_links=True,
    )
    return Membership.ListResponse(
        memberships=[
            Membership.Response(
                id=membership.id,
                org=Organization.Response(
                    id=membership.org.id,
                    name=membership.org.name,
                ),
                user=User.Response(
                    id=membership.user.id,
                    name=membership.user.name,
                    email=membership.user.email,
                ),
                status=membership.status,
            )
            for membership in memberships
        ]
    )


@router.patch("/invites/{membership_id}")
async def accept_invite(
    membership_id: PydanticObjectId,
    user: User = Depends(get_authed_user),
    membership_service: MembershipService = Depends(MembershipService),
) -> Membership.Response:
    """Accept a membership invite from an organization."""
    # check if membership exists and is an invite for the user
    membership = await membership_service.get(membership_id=membership_id)
    if not membership:
        raise NotFoundException("That invitation was not found.")
    if membership.user.ref.id != user.id:
        raise ValidationException("You were not invited to this organization.")
    if membership.status != "pending":
        raise ValidationException("You have already accepted this invitation.")
    # update membership status
    membership = await membership_service.update(Membership.Update(status="approved"))
    assert membership is not None
    await membership.fetch_link("org")
    await membership.fetch_link("user")
    return Membership.Response(
        id=membership.id,
        org=Organization.Response(
            id=membership.org.id,
            name=membership.org.name,
        ),
        user=User.Response(
            id=membership.user.id,
            name=membership.user.name,
            email=membership.user.email,
        ),
        status=membership.status,
    )


@router.delete("/invites/{membership_id}")
async def cancel_invite(
    membership_id: PydanticObjectId,
    user: User = Depends(get_authed_user),
    membership_service: MembershipService = Depends(MembershipService),
) -> Membership.Response:
    """Cancel a membership invite."""
    # check if user is in organization to be cancelling invite
    membership = await membership_service.get(membership_id=membership_id)
    if not membership:
        raise NotFoundException("That invitation was not found.")
    if not await membership_service.get(
        org_id=membership.org.ref.id,
        user_id=user.id,
    ):
        raise ValidationException("You are not a member of this organization.")
    # delete membership
    membership = await membership_service.delete(membership_id=membership_id)
    assert membership is not None
    await membership.fetch_link("org")
    await membership.fetch_link("user")
    return Membership.Response(
        id=membership.id,
        org=Organization.Response(
            id=membership.org.id,
            name=membership.org.name,
        ),
        user=User.Response(
            id=membership.user.id,
            name=membership.user.name,
            email=membership.user.email,
        ),
        status=membership.status,
    )
