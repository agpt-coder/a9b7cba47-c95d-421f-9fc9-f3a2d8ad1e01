from typing import Any, Dict, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class CreateTemplateResponse(BaseModel):
    """
    Response confirming the successful creation of the template or providing error feedback.
    """

    success: bool
    message: str
    template_id: Optional[str] = None


async def create_template(
    title: str,
    description: Optional[str],
    content: Dict[str, Any],
    user_id: Optional[str],
) -> CreateTemplateResponse:
    """
    Allows users to create a new template.

    Args:
    title (str): The title of the template.
    description (Optional[str]): A brief description of what the template is used for.
    content (Dict[str, Any]): Structured content of the template, defined in a format that the AI can understand and utilize for generating templates dynamically based on the user's role and the project's context.
    user_id (Optional[str]): The ID of the user creating the template. This might be extracted automatically from the authentication token and thus not required in the request body directly.

    Returns:
    CreateTemplateResponse: Response confirming the successful creation of the template or providing error feedback.
    """
    try:
        new_template = await prisma.models.Template.prisma().create(
            data={
                "title": title,
                "description": description,
                "content": content,
                "userId": user_id,
            }
        )
        return CreateTemplateResponse(
            success=True,
            message="Template created successfully.",
            template_id=new_template.id,
        )
    except Exception as error:
        return CreateTemplateResponse(
            success=False,
            message=f"Failed to create template: {error}",
            template_id=None,
        )
