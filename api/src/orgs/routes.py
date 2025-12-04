from fastapi import APIRouter, Depends

from api.src.orgs.service import OrgService
from api.src.orgs.types import Organization
from api.src.user_orgs.service import UserOrgService

router = APIRouter(prefix="/orgs", tags=["orgs"])


@router.get("/{org_name}", response_model=Organization.Response)
async def get_org(
    org_name: str,
    org_service: OrgService = Depends(OrgService),
    user_org_service: UserOrgService = Depends(UserOrgService),
):
    """Get organization details by name."""
    db_org = await org_service.get_by_name(org_name)
    db_user_orgs = await user_org_service.get_all_by_org_id(
        org_id=db_org.id, status="approved"
    )
    for db_user_org in db_user_orgs:
        await db_user_org.fetch_link("user")
    return {
        "id": db_org.id,
        "name": db_org.name,
        "users": [
            {
                "id": db_user_org.user.id,
                "name": db_user_org.user.name,
                "email": db_user_org.user.email,
            }
            for db_user_org in db_user_orgs
        ],
    }


@router.post("/", response_model=Organization.Response)
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
