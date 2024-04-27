import logging
from contextlib import asynccontextmanager
from typing import Any, Dict, Optional

import project.create_user_service
import project.discover_devices_service
import project.login_user_service
import project.register_device_service
import project.update_device_configuration_service
import project.update_user_service
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
    title="xhom",
    lifespan=lifespan,
    description="Our Smart Home Central Control Dashboard is designed using the Flask web framework as its core with Python. It utilizes an application entry point named `app.py` that sets up Flask and incorporates routes from `routes.py` for mapping URL paths such as `/dashboard` for the main control panel access and `/devices/{id}/control` for specific device operations. The `dashboard_controller.py` is responsible for retrieving information about all connected devices from `device_model.py`, which interacts with MongoDB through an ORM-like mechanism allowing for flexible database interactions. Device commands and operations are managed via `device_control.py`, communicating with smart devices using a universal API adapter. The device and user settings, including automated routine scripts, are maintained in MongoDB through `device_model.py`, facilitating dynamic schema modifications. The frontend is powered by Vue.js, offering a reactive and component-based structure, enriched with Vuex for state management and Vue Router for single-page application (SPA) features. AJAX calls are implemented within Vue components to provide a seamless user experience with real-time feedback. Additionally, voice command features are incorporated through `voice_handlers.py`, leveraging voice assistant APIs like those from Google Assistant or Amazon Alexa to convert spoken commands into dashboard actions. This configuration not only streamlines home automation management for users but also lays down a strong, scalable foundation for further advancements and integrations within the Internet of Things (IoT) ecosystem.",
)


@app.post("/user/login", response_model=project.login_user_service.UserLoginResponse)
async def api_post_login_user(
    username: str, password: str
) -> project.login_user_service.UserLoginResponse | Response:
    """
    Authenticates a user and returns an access token.
    """
    try:
        res = await project.login_user_service.login_user(username, password)
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
    "/user/update", response_model=project.update_user_service.UpdateUserProfileResponse
)
async def api_put_update_user(
    id: str, email: Optional[str], name: Optional[str], password: Optional[str]
) -> project.update_user_service.UpdateUserProfileResponse | Response:
    """
    Updates user profile information.
    """
    try:
        res = await project.update_user_service.update_user(id, email, name, password)
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
    "/user/register", response_model=project.create_user_service.CreateUserResponse
)
async def api_post_create_user(
    email: str, password: str, preferences: Dict[str, str]
) -> project.create_user_service.CreateUserResponse | Response:
    """
    Creates a new user account.
    """
    try:
        res = await project.create_user_service.create_user(
            email, password, preferences
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
    "/devices/discover",
    response_model=project.discover_devices_service.DiscoverDevicesResponse,
)
async def api_get_discover_devices() -> project.discover_devices_service.DiscoverDevicesResponse | Response:
    """
    List all discoverable devices in the network.
    """
    try:
        res = project.discover_devices_service.discover_devices()
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
    "/devices/register",
    response_model=project.register_device_service.RegisterDeviceResponse,
)
async def api_post_register_device(
    name: str, deviceType: str, initialConfig: Dict[str, str]
) -> project.register_device_service.RegisterDeviceResponse | Response:
    """
    Registers a new device with the system.
    """
    try:
        res = await project.register_device_service.register_device(
            name, deviceType, initialConfig
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
    "/devices/{id}/configure",
    response_model=project.update_device_configuration_service.UpdateDeviceConfigurationResponse,
)
async def api_put_update_device_configuration(
    id: str, configuration: Dict[str, Any]
) -> project.update_device_configuration_service.UpdateDeviceConfigurationResponse | Response:
    """
    Updates the configuration for a specific device.
    """
    try:
        res = await project.update_device_configuration_service.update_device_configuration(
            id, configuration
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
