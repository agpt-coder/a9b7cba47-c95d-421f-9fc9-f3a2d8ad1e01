from datetime import datetime
from uuid import uuid4

import prisma
import prisma.models
from pydantic import BaseModel


class InitiateDialogueResponse(BaseModel):
    """
    Provides details about the initiated dialogue session, including session ID and any initial AI-driven responses or prompts for further information.
    """

    session_id: str
    ai_prompt: str
    status: str


async def initiate_dialogue(
    user_id: str, initial_query: str, context: str
) -> InitiateDialogueResponse:
    """
    Starts a new dialogue session.

    Args:
    user_id (str): Unique identifier for the user initiating the dialogue.
    initial_query (str): Initial user query or statement needing clarification or refinement.
    context (str): Additional context that might help in tailoring the dialogue.

    Returns:
    InitiateDialogueResponse: Provides details about the initiated dialogue session, including session ID and any initial AI-driven responses or prompts for further information.

    """
    session_id = str(uuid4())
    ai_prompt = f"To better assist you, could you please clarify your request in the context of {context}?"
    dialogue = await prisma.models.Dialogue.prisma().create(
        data={
            "id": session_id,
            "sessionId": session_id,
            "startTimestamp": datetime.now(),
            "dialogues": {
                "initial_query": initial_query,
                "context": context,
                "ai_prompt": ai_prompt,
            },
            "status": "IN_PROGRESS",
            "userId": user_id,
        }
    )
    if dialogue:
        return InitiateDialogueResponse(
            session_id=session_id, ai_prompt=ai_prompt, status="active"
        )
    raise Exception("Failed to initiate dialogue session")
