from typing import Any, Dict

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class ContinueDialogueOutput(BaseModel):
    """
    This model represents the system's response after processing the new user input for the specified session. It includes the updated session information and any immediate response or action the system has generated.
    """

    sessionId: str
    dialogueStatus: str
    systemResponse: str
    nextExpectedInputType: str


async def continue_dialogue(sessionId: str, userInput: str) -> ContinueDialogueOutput:
    """
    Continues an existing dialogue session.

    Args:
      sessionId (str): A unique identifier for the dialogue session that is being continued.
      userInput (str): The new input from the user that needs to be processed to continue the dialogue.

    Returns:
      ContinueDialogueOutput: This model represents the system's response after processing the new user input for the specified session. It includes the updated session information and any immediate response or action the system has generated.
    """
    dialogue = await prisma.models.Dialogue.prisma().find_unique(
        where={"sessionId": sessionId}
    )
    if dialogue is None:
        raise ValueError(f"No dialogue found with session ID: {sessionId}")
    updated_dialogues_json: Dict[str, Any] = {
        **dialogue.dialogues,
        "latest_input": userInput,
    }
    await prisma.models.Dialogue.prisma().update(
        where={"sessionId": sessionId},
        data={
            "status": prisma.enums.DialogueStatus.IN_PROGRESS,
            "dialogues": updated_dialogues_json,
        },
    )
    return ContinueDialogueOutput(
        sessionId=sessionId,
        dialogueStatus="IN_PROGRESS",
        systemResponse="Your input has been processed. What else can I assist you with?",
        nextExpectedInputType="More detailed information or further queries.",
    )
