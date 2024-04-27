from datetime import datetime, timedelta
from typing import Optional

import prisma
import prisma.models
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel


class UserLoginResponse(BaseModel):
    """
    This model defines the response structure for a successful user login, containing a secure token for the authenticated session.
    """

    token: str
    expiry: datetime


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "A VERY SECRET KEY"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hashed version.

    Args:
    plain_password (str): Plain text password.
    hashed_password (str): Hashed password.

    Returns:
    bool: True if password matches the hash, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


async def get_user(username: str) -> Optional[prisma.models.User]:
    """
    Fetches a user by username (in this context, username is the email).

    Args:
    username (str): The username (email) of the user to fetch.

    Returns:
    Optional[prisma.models.User]: The user object if found, None otherwise.
    """
    return await prisma.models.User.prisma().find_unique(where={"email": username})


async def create_access_token(
    *, data: dict, expires_delta: timedelta = timedelta(minutes=15)
) -> str:
    """
    Creates an access JWT token with expiration.

    Args:
    data (dict): The data to encode in the token.
    expires_delta (timedelta): The lifetime of the token.

    Returns:
    str: The generated JWT token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def login_user(username: str, password: str) -> UserLoginResponse:
    """
    Authenticates a user and returns an access token.

    Args:
    username (str): The username of the user attempting to log in.
    password (str): The password of the user attempting to log in.

    Returns:
    UserLoginResponse: This model defines the response structure for a successful user login, containing a secure token for the authenticated session.
    """
    user = await get_user(username)
    if user and await verify_password(password, user.password):
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = await create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        return UserLoginResponse(
            token=access_token, expiry=datetime.utcnow() + access_token_expires
        )
    raise Exception("Invalid login attempt")
