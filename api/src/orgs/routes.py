from fastapi import APIRouter, Depends

from api.src.memberships.service import MembershipService
from api.src.orgs.service import OrgService
from api.src.orgs.types import Organization

router = APIRouter(prefix="/orgs", tags=["orgs"])


@router.get("/{org_name}", response_model=Organization.DetailResponse)
async def get_org(
    org_name: str,
    org_service: OrgService = Depends(OrgService),
    membership_service: MembershipService = Depends(MembershipService),
):
    """Get organization details by name."""
    db_org = await org_service.get_by_name(org_name)
    db_memberships = await membership_service.get_all_by_org_id(
        org_id=db_org.id, status="approved"
    )
    for db_membership in db_memberships:
        await db_membership.fetch_link("user")
    return {
        "id": db_org.id,
        "name": db_org.name,
        "users": [
            {
                "id": db_membership.user.id,
                "name": db_membership.user.name,
                "email": db_membership.user.email,
            }
            for db_membership in db_memberships
        ],
    }


@router.post("/", response_model=Organization.DetailResponse)
async def create_org(
    org: Organization.Create,
    org_service: OrgService = Depends(OrgService),
):
    """Create a new organization."""
    db_org = await org_service.create(org)
    return {
        "id": db_org.id,
        "name": db_org.name,
    }
