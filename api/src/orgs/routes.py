from fastapi import APIRouter, Depends

from api.core.exceptions import NotFoundException
from api.src.auth.auth0 import get_authed_user
from api.src.memberships.service import MembershipService
from api.src.memberships.types import Membership
from api.src.orgs.service import OrgService
from api.src.orgs.types import Organization
from api.src.users.types import User

router = APIRouter(prefix="/orgs", tags=["orgs"])


@router.get("/{org_name}")
async def get_org(
    org_name: str,
    user: User = Depends(get_authed_user),
    org_service: OrgService = Depends(OrgService),
    membership_service: MembershipService = Depends(MembershipService),
) -> Organization.DetailResponse:
    """Get organization details by name."""
    db_org = await org_service.get(org_name=org_name)
    if not db_org:
        raise NotFoundException("Organization not found.")
    if not await membership_service.get(
        org_id=db_org.id,
        user_id=user.id,
        status="approved",
    ):
        raise NotFoundException("You are not a member of this organization.")
    db_memberships = await membership_service.get_all(
        org_id=db_org.id, status="approved"
    )
    for db_membership in db_memberships:
        await db_membership.fetch_link("user")
    return Organization.DetailResponse(
        id=db_org.id,
        name=db_org.name,
        users=[
            User.Response(
                id=db_membership.user.id,
                name=db_membership.user.name,
                email=db_membership.user.email,
            )
            for db_membership in db_memberships
        ],
    )


@router.post("/")
async def create_org(
    org: Organization.Create,
    user: User = Depends(get_authed_user),
    org_service: OrgService = Depends(OrgService),
    membership_service: MembershipService = Depends(MembershipService),
) -> Organization.DetailResponse:
    """Create a new organization."""
    db_org = await org_service.create(org)
    # could be done in a single operation, but orgs are not created that often
    membership = await membership_service.create(
        Membership.Create(
            org_id=db_org.id,
            user_id=user.id,
        )
    )
    await membership_service.update(Membership.Update(status="approved"))
    await membership.fetch_link("user")
    return Organization.DetailResponse(
        id=db_org.id,
        name=db_org.name,
        users=[
            User.Response(
                id=membership.user.id,
                name=membership.user.name,
                email=membership.user.email,
            )
        ],
    )
