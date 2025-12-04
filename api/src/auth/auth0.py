
import jwt
from fastapi import Depends
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from api.core.config import settings
from api.core.exceptions import (
    ForbiddenException,
    UnauthorizedException,
)
from api.src.users.service import UserService
from api.src.users.types import User


def _extract_auth0_id_email_name_from_token(
    token: HTTPAuthorizationCredentials | None,
):
    if token:
        try:
            jwks_url = f"https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json"
            jwks_client = jwt.PyJWKClient(jwks_url)
            signing_key = jwks_client.get_signing_key_from_jwt(token.credentials).key
            payload = jwt.decode(
                token.credentials,
                signing_key,
                algorithms=settings.AUTH0_ALGORITHMS,
                audience=settings.AUTH0_API_AUDIENCE,
                issuer=settings.AUTH0_ISSUER,
            )
            auth0_id = payload.get("sub")
            if auth0_id is None:
                raise UnauthorizedException(detail="Missing sub claim in auth token")
            custom_claim = (
                settings.AUTH0_API_AUDIENCE + "/"
                if not settings.AUTH0_API_AUDIENCE.endswith("/")
                else settings.AUTH0_API_AUDIENCE
            )
            email = payload.get(custom_claim + "email")
            if email is None:
                raise UnauthorizedException(
                    detail="Missing email custom claim in auth token"
                )
            name = payload.get(custom_claim + "name")
            if name is None:
                name = email.split("@")[0]
            return auth0_id, email, name
        except jwt.exceptions.PyJWTError as error:
            raise UnauthorizedException(detail=str(error)) from error
    else:
        if settings.ENABLE_FAKE_AUTH:
            auth0_id = "fake_auth0_id"
            email = "fake@auth0.com"
            name = "Fake Auth0 User"
            return auth0_id, email, name
        else:
            raise ForbiddenException


async def get_current_user(
    token: HTTPAuthorizationCredentials | None = Depends(
        HTTPBearer(auto_error=False)
    ),
) -> User:
    auth0_id, email, name = _extract_auth0_id_email_name_from_token(token)
    user = await UserService().upsert_by_auth0_id(
        auth0_id=auth0_id, user_update=User.Update(name=name, email=email)
    )
    return user
