import logging
from contextlib import asynccontextmanager
from typing import Any, Dict, Optional

import project.continue_dialogue_service
import project.create_template_service
import project.edit_profile_service
import project.fetch_templates_service
import project.initiate_dialogue_service
import project.login_user_service
import project.register_user_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="a",
    lifespan=lifespan,
    description="It appears there has been a consistent misunderstanding in our communication. The responses reveal a pattern where the nature of the assistance required was not clarified despite multiple attempts. The user consistently indicated a broad capability to provide support and assistance across a variety of tasks and topics, such as software development, technology guidance, and more. However, a specific query or task from the user's end was never articulated. In essence, the user communicated their readiness to offer detailed support in numerous areas, including but not limited to software application development, data analysis, web development, technology advice, and educational content, but did not specify a particular project or question that requires assistance. This cyclical communication underscores the importance of clear and precise queries when seeking assistance to ensure effective and targeted support.",
)


@app.post(
    "/user/register",
    response_model=project.register_user_service.UserRegistrationResponse,
)
async def api_post_register_user(
    email: str, password: str, role: Optional[project.register_user_service.Role]
) -> project.register_user_service.UserRegistrationResponse | Response:
    """
    Registers a new user.
    """
    try:
        res = await project.register_user_service.register_user(email, password, role)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/dialogue/initiate",
    response_model=project.initiate_dialogue_service.InitiateDialogueResponse,
)
async def api_post_initiate_dialogue(
    user_id: str, initial_query: str, context: str
) -> project.initiate_dialogue_service.InitiateDialogueResponse | Response:
    """
    Starts a new dialogue session.
    """
    try:
        res = await project.initiate_dialogue_service.initiate_dialogue(
            user_id, initial_query, context
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/template/create",
    response_model=project.create_template_service.CreateTemplateResponse,
)
async def api_post_create_template(
    title: str,
    description: Optional[str],
    content: Dict[str, Any],
    user_id: Optional[str],
) -> project.create_template_service.CreateTemplateResponse | Response:
    """
    Allows users to create a new template.
    """
    try:
        res = await project.create_template_service.create_template(
            title, description, content, user_id
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/user/edit", response_model=project.edit_profile_service.UserProfileUpdateResponse
)
async def api_put_edit_profile(
    id: str,
    email: Optional[str],
    username: Optional[str],
    bio: Optional[str],
    phoneNumber: Optional[str],
) -> project.edit_profile_service.UserProfileUpdateResponse | Response:
    """
    Edits user profile information.
    """
    try:
        res = await project.edit_profile_service.edit_profile(
            id, email, username, bio, phoneNumber
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/user/login", response_model=project.login_user_service.UserLoginResponse)
async def api_post_login_user(
    email: str, password: str
) -> project.login_user_service.UserLoginResponse | Response:
    """
    Authenticates a user.
    """
    try:
        res = await project.login_user_service.login_user(email, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/dialogue/continue",
    response_model=project.continue_dialogue_service.ContinueDialogueOutput,
)
async def api_post_continue_dialogue(
    sessionId: str, userInput: str
) -> project.continue_dialogue_service.ContinueDialogueOutput | Response:
    """
    Continues an existing dialogue session.
    """
    try:
        res = await project.continue_dialogue_service.continue_dialogue(
            sessionId, userInput
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/template/fetch",
    response_model=project.fetch_templates_service.FetchTemplatesResponse,
)
async def api_get_fetch_templates(
    user_id: str,
) -> project.fetch_templates_service.FetchTemplatesResponse | Response:
    """
    Retrieves a list of templates for the user.
    """
    try:
        res = await project.fetch_templates_service.fetch_templates(user_id)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
