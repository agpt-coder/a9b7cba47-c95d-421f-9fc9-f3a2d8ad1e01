from typing import List, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class Template(BaseModel):
    """
    A template object representing a customizable query template for the user.
    """

    id: str
    title: str
    description: Optional[str] = None
    content: str
    role_specific: bool
    created_at: str
    updated_at: Optional[str] = None


class FetchTemplatesResponse(BaseModel):
    """
    Response model containing the list of templates available to the user, formatted according to their role and project context.
    """

    templates: List[Template]


async def fetch_templates(user_id: str) -> FetchTemplatesResponse:
    """
    Retrieves a list of templates for the user.

    Args:
        user_id (str): Unique identifier of the user for whom templates are being fetched. This value is typically extracted from the authentication token and does not directly come from the client request.

    Returns:
        FetchTemplatesResponse: Response model containing the list of templates available to the user, formatted according to their role and project context.
    """
    prisma_templates = await prisma.models.Template.prisma().find_many(
        where={"userId": user_id}
    )
    templates = [
        Template(
            id=template.id,
            title=template.title,
            description=template.description,
            content=template.content,
            role_specific=False,
            created_at=template.createdAt.isoformat(),
            updated_at=template.updatedAt.isoformat() if template.updatedAt else None,
        )
        for template in prisma_templates
    ]
    return FetchTemplatesResponse(templates=templates)
