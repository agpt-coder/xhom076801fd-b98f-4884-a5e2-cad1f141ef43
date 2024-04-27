from typing import Dict

import prisma
import prisma.models
from pydantic import BaseModel


class RegisterDeviceResponse(BaseModel):
    """
    The response model confirming the successful registration of a device and its generated identifiers within the HomeSphere system.
    """

    deviceId: str
    name: str
    deviceType: str
    registrationStatus: str


async def register_device(
    name: str, deviceType: str, initialConfig: Dict[str, str]
) -> RegisterDeviceResponse:
    """
    Registers a new device with the system.

    Args:
        name (str): The name of the device being registered.
        deviceType (str): A string indicating the type of the device (e.g., 'light', 'thermostat').
        initialConfig (Dict[str, str]): Initial configuration settings for the device,
                                         expressed as a dictionary.

    Returns:
        RegisterDeviceResponse: The response model confirming the successful registration of a device
                                and its generated identifiers within the system.
    """
    device = await prisma.models.Device.prisma().create(
        data={"name": name, "deviceType": deviceType, "isOnline": False}
    )
    return RegisterDeviceResponse(
        deviceId=device.id,
        name=device.name,
        deviceType=device.deviceType,
        registrationStatus="success",
    )
