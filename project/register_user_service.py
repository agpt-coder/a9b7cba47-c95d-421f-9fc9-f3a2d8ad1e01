from enum import Enum
from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class Role(Enum):
    """
    Enumeration of possible user roles within the system.
    """

    STUDENT: str
    TUTOR: str
    ADMIN: str


class UserRegistrationResponse(BaseModel):
    """
    Response model for user registration. Contains basic information about the created user.
    """

    id: str
    email: str
    role: Role
    message: str


async def register_user(
    email: str, password: str, role: Optional[Role] = Role.STUDENT
) -> UserRegistrationResponse:
    """
    Registers a new user.

    This function is responsible for creating a new user with the given email, password, and role.
    If no role is specified, the user is assigned the role of STUDENT by default.

    Args:
        email (str): Email address of the new user. This will be used as their username for login purposes.
        password (str): Password for the new user account. Should follow best practices for security (e.g., minimum length).
        role (Optional[Role]): The initial role of the user within the system. Defaults to STUDENT if not specified.

    Returns:
        UserRegistrationResponse: Response model for user registration. Contains basic information about the created user,
        including a success message.

    """
    user = await prisma.models.User.prisma().create(
        data={"email": email, "password": password, "role": role.value}
    )
    return UserRegistrationResponse(
        id=user.id,
        email=user.email,
        role=Role(user.role),
        message="User created successfully.",
    )
