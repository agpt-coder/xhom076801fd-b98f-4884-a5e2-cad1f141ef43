from typing import List, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class UpdateUserProfileResponse(BaseModel):
    """
    Acknowledges the update of user profile information. Can optionally return the updated information.
    """

    success: bool
    id: str
    updatedFields: Optional[List[str]] = None


async def update_user(
    id: str,
    email: Optional[str] = None,
    name: Optional[str] = None,
    password: Optional[str] = None,
) -> UpdateUserProfileResponse:
    """
    Updates user profile information in the database, based on the provided user ID and the fields to be updated.
    Fields not specified are left unchanged. Password should be hashed if provided.

    Args:
        id (str): The unique identifier for the user.
        email (Optional[str], optional): The new email address for the user. Defaults to None.
        name (Optional[str], optional): The new name of the user. Defaults to None.
        password (Optional[str], optional): The new hashed password for the user. Defaults to None.

    Returns:
        UpdateUserProfileResponse: An instance containing the result of the update operation, including success
        status, user ID, and a list of updated fields.
    """
    updatedFields = []
    update_data = {}
    if email is not None:
        update_data["email"] = email
        updatedFields.append("email")
    if name is not None:
        update_data["name"] = name
        updatedFields.append("name")
    if password is not None:
        update_data["password"] = password
        updatedFields.append("password")
    if update_data:
        await prisma.models.User.prisma().update(where={"id": id}, data=update_data)
    return UpdateUserProfileResponse(
        success=True, id=id, updatedFields=updatedFields if updatedFields else None
    )
