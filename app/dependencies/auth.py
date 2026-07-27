from typing import Annotated

from fastapi import Depends
from jose import JWTError

from app.core.security import decode_access_token, oauth2_scheme
from app.dependencies.database import DBSession
from app.exceptions import InvalidTokenException
from app.models.user import User
from app.repositories.user_repository import UserRepository


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: DBSession,
) -> User:
    try:
        payload = decode_access_token(token)
        user_id_str: str | None = payload.get("sub")
        if user_id_str is None:
            raise InvalidTokenException()
        user_id = int(user_id_str)
    except (JWTError, ValueError):
        raise InvalidTokenException()

    user_repo = UserRepository(db)
    user = user_repo.find_by_id(user_id)
    if user is None:
        raise InvalidTokenException()

    return user


CurrentUserDep = Annotated[
    User,
    Depends(get_current_user)
]
