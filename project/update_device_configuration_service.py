from typing import Any, Dict

import prisma
import prisma.models
from pydantic import BaseModel


class UpdateDeviceConfigurationResponse(BaseModel):
    """
    The response model confirming the device configuration has been successfully updated, including the new configuration details.
    """

    success: bool
    device_id: str
    new_configuration: Dict[str, Any]
    message: str


async def update_device_configuration(
    id: str, configuration: Dict[str, Any]
) -> UpdateDeviceConfigurationResponse:
    """
    Updates the configuration for a specific device.

    Args:
        id (str): The unique identifier of the device to be configured.
        configuration (Dict[str, Any]): A JSON object containing the new configuration settings for the device.

    Returns:
        UpdateDeviceConfigurationResponse: The response model confirming the device configuration has been successfully updated, including the new configuration details.

    Example:
        If the device with id "some_device_id" exists and the configuration update is successful, then the function will return:
        UpdateDeviceConfigurationResponse(success=True, device_id="some_device_id", new_configuration={"volume": "low", "brightness": "medium"}, message="Device configuration updated successfully.")
    """
    device = await prisma.models.Device.prisma().find_unique(where={"id": id})
    if not device:
        return UpdateDeviceConfigurationResponse(
            success=False,
            device_id=id,
            new_configuration=configuration,
            message="Device not found.",
        )
    try:
        await prisma.models.Control.prisma().create(
            {"deviceId": id, "value": configuration, "command": "UpdateConfiguration"}
        )
        return UpdateDeviceConfigurationResponse(
            success=True,
            device_id=id,
            new_configuration=configuration,
            message="Device configuration updated successfully.",
        )
    except Exception as e:
        return UpdateDeviceConfigurationResponse(
            success=False,
            device_id=id,
            new_configuration=configuration,
            message=f"Failed to update device configuration. Error: {str(e)}",
        )
