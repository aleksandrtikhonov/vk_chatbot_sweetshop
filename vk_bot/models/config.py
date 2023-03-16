from __future__ import annotations

from typing import Self

from django.db.models import QuerySet, Model, BooleanField
from enumchoicefield import EnumChoiceField

from vk_bot.models.types import BotConfigsEnum


class BotConfigsQs(QuerySet):
    def get_config_value(self, config_name: BotConfigsEnum) -> bool:
        return self.get(name=config_name).value

    def set_config_value(self, config_name: BotConfigsEnum, value: bool) -> None:
        qs: Self = self.filter(name=config_name)
        qs.update(value=value)


class BotConfigs(Model):
    class Meta:
        db_table = 'bot_config'
        verbose_name = 'Конфигурация бота'
        verbose_name_plural = 'Конфигурации бота'

    name: EnumChoiceField = EnumChoiceField(BotConfigsEnum)
    value: bool = BooleanField(default=False)
    # TODO Для расширения функционала нужно поле type для парсинга типа value(int, str, ...).

    objects: BotConfigsQs[BotConfigs] = BotConfigsQs.as_manager()
