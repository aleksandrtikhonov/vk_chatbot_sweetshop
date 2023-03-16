from __future__ import annotations

from typing import NewType

from enumchoicefield import ChoiceEnum

ProductId = NewType('ProductId', int)


class BotConfigsEnum(ChoiceEnum):
    new_keyboard_exists = "new_keyboard_exists"
