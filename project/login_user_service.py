from datetime import datetime, timedelta
from typing import Optional

import bcrypt
import jwt
import prisma
import prisma.models
from pydantic import BaseModel


class UserLoginResponse(BaseModel):
    """
    Response model for user login. Indicates whether the login was successful and provides a token for authenticated sessions.
    """

    success: bool
    message: str
    token: Optional[str] = None


async def login_user(email: str, password: str) -> UserLoginResponse:
    """
    Authenticates a user by verifying their email and password against the database.
    If authentication is successful, generates a JWT token for the session.

    Args:
    email (str): The email address of the user attempting to log in.
    password (str): The password of the user attempting to log in. This will be hashed and compared against the stored hash in the database.

    Returns:
    UserLoginResponse: Response model for user login. Indicates whether the login was successful and provides a token for authenticated sessions.

    Example:
        response = await login_user("user@example.com", "password123")
        > UserLoginResponse(success=True, message="Login successful.", token="<JWT_TOKEN>")
    """
    user = await prisma.models.User.prisma().find_unique(where={"email": email})
    if user and bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
        SECRET_KEY = "YOUR_SECRET_KEY"
        ALGORITHM = "HS256"
        expire = datetime.utcnow() + timedelta(days=1)
        token_data = {"sub": user.id, "exp": expire}
        token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
        return UserLoginResponse(success=True, message="Login successful.", token=token)
    else:
        return UserLoginResponse(
            success=False, message="Invalid email or password.", token=None
        )
