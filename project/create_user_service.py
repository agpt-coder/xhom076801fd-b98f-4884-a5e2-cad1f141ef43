import json
from typing import Dict

import bcrypt
import prisma
import prisma.models
from pydantic import BaseModel


class CreateUserResponse(BaseModel):
    """
    The response model to confirm the creation of a new user account and provide basic information back to the client.
    """

    user_id: str
    email: str
    message: str


async def create_user(
    email: str, password: str, preferences: Dict[str, str]
) -> CreateUserResponse:
    """
    Creates a new user account by hashing the password, storing the user's information and their preferences in the database.

    Args:
        email (str): The email address for the user account. This will be used as the unique identifier for login.
        password (str): The password for the user account, which will be securely stored after hashing.
        preferences (Dict[str, str]): Optional preferences for the user account which could include UI preferences, notification settings, or any other user-specific settings.

    Returns:
        CreateUserResponse: The response model to confirm the creation of a new user account and provide basic information back to the client.

    Raises:
        Exception: If there's an error during the creation process, such as if the email already exists in the database.

    Example:
        create_user_response = await create_user("test@example.com", "securepassword123", {"theme": "dark", "notifications": "enabled"})
        print(create_user_response)
        > CreateUserResponse(user_id='...', email='test@example.com', message='User created successfully.')
    """
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode(
        "utf-8"
    )
    existing_user = await prisma.models.User.prisma().find_unique(
        where={"email": email}
    )
    if existing_user:
        raise Exception("Email already exists in the database")
    user = await prisma.models.User.prisma().create(
        data={"email": email, "password": hashed_password, "role": "USER"}
    )
    await prisma.models.UserSettings.prisma().create(
        data={"userId": user.id, "settings": json.dumps(preferences)}
    )
    return CreateUserResponse(
        user_id=user.id, email=user.email, message="User created successfully."
    )
