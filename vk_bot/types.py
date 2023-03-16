from enum import StrEnum
from typing import NewType, Union

from vk_bot.models import ProductsCategory


class MessageTypes(StrEnum):
    NEW_MESSAGE: str = 'message_new'


NextLevel = NewType('NextLevel', Union[str, int, ProductsCategory])
Button = NewType('Button', Union[dict[str, dict[str, str]], list[str, dict[str, str]]])
MenuScreen = NewType('MenuScreen', dict[str, bool | list[Button]])
