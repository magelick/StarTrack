from sqlalchemy import select

from starlette.authentication import (
    AuthenticationBackend,
    AuthCredentials,
    BaseUser,
)
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.requests import HTTPConnection

from src.database.models import User
from src.settings import SETTINGS
from src.utils import verify_access_token


class UserInfo(BaseUser):
    """
    Class User info
    """

    def __init__(self, user: User):
        self.user = user

    @property
    def is_authenticated(self) -> bool:
        """
        User is authenticated or not
        :return:
        """
        return True

    @property
    def identity(self) -> int:  # type: ignore
        """
        Return User ID
        :return:
        """
        return int(self.user.id)


class JWTAuthenticationBackend(AuthenticationBackend):
    """
    Middleware class for authentication user
    """

    async def authenticate(
        self, conn: HTTPConnection
    ) -> tuple[AuthCredentials, UserInfo] | None:
        """
        Check authenticate user
        :param conn:
        :return:
        """
        auth = (
            conn.headers.get("Authorization")
            if "Authorization" in conn.headers
            else conn.headers.get("authorization")
        )

        if not auth or not auth.startswith(f"{SETTINGS.TOKEN_TYPE}"):
            return  # type: ignore

        token = auth.replace(f"{SETTINGS.TOKEN_TYPE}", "").lstrip()

        payload = await verify_access_token(access_token=token)

        if not payload:
            return  # type: ignore
        else:
            async with User.async_session_maker() as session:
                user = await session.scalar(
                    select(User).filter_by(id=int(payload.get("sub")))
                )

                if not user:
                    return  # type: ignore
                else:
                    return AuthCredentials(["authenticated"]), UserInfo(
                        user=user
                    )


# Initial middlewares
MIDDLEWARES = (
    (AuthenticationMiddleware, {"backend": JWTAuthenticationBackend()}),
)
