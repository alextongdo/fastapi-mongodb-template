from fastapi import APIRouter, Depends

from api.src.memberships.service import MembershipService
from api.src.orgs.service import OrgService
from api.src.orgs.types import Organization
from api.src.users.types import User

router = APIRouter(prefix="/orgs", tags=["orgs"])


@router.get("/{org_name}")
async def get_org(
    org_name: str,
    org_service: OrgService = Depends(OrgService),
    membership_service: MembershipService = Depends(MembershipService),
) -> Organization.DetailResponse:
    """Get organization details by name."""
    db_org = await org_service.get(org_name=org_name)
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
    org_service: OrgService = Depends(OrgService),
) -> Organization.DetailResponse:
    """Create a new organization."""
    db_org = await org_service.create(org)
    return Organization.DetailResponse(
        id=db_org.id,
        name=db_org.name,
        users=[],
    )
