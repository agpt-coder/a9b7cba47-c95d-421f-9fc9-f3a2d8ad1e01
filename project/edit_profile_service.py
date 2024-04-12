from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class UserProfileUpdateResponse(BaseModel):
    """
    Response model for the profile update operation, including success state and any relevant error messages.
    """

    success: bool
    message: str


async def edit_profile(
    id: str,
    email: Optional[str],
    username: Optional[str],
    bio: Optional[str],
    phoneNumber: Optional[str],
) -> UserProfileUpdateResponse:
    """
    Edits user profile information.

    Args:
    id (str): The user's unique identifier, used to fetch the correct user record for updates.
    email (Optional[str]): The user's new email address, optional for update.
    username (Optional[str]): The new username the user wishes to adopt, optional for update.
    bio (Optional[str]): A short bio or description the user wants to set on their profile, optional for update.
    phoneNumber (Optional[str]): The user's updated phone number, optional for update.

    Returns:
    UserProfileUpdateResponse: Response model for the profile update operation, including success state and any relevant error messages.
    """
    try:
        user = await prisma.models.User.prisma().find_unique(where={"id": id})
        if not user:
            return UserProfileUpdateResponse(
                success=False, message=f"User with ID {id} not found."
            )
        update_data = {}
        if email is not None:
            update_data["email"] = email
        if username is not None:
            update_data["name"] = username
        if bio is not None:
            update_data["bio"] = bio
        if phoneNumber is not None:
            update_data["phoneNumber"] = phoneNumber
        updated_user = await prisma.models.User.prisma().update(
            where={"id": id}, data=update_data
        )
        return UserProfileUpdateResponse(
            success=True, message="User profile updated successfully."
        )
    except Exception as e:
        return UserProfileUpdateResponse(
            success=False, message=f"Error updating user profile: {str(e)}"
        )
