from django.contrib.admin import ModelAdmin, register

from vk_bot.models.categories import ProductsCategory
from vk_bot.models.config import BotConfigs
from vk_bot.models.product import Products
from vk_bot.models.types import BotConfigsEnum


class ShowCaseAdmin(ModelAdmin):
    list_display = ('pk', 'name', 'is_active')
    list_filter = ('name', 'is_active')
    search_fields = ('name', 'is_active')


@register(Products)
class ProductAdmin(ShowCaseAdmin):
    list_display = ('pk', 'name', 'category', 'is_active', 'description', 'vk_photo_id')


@register(ProductsCategory)
class ProductsCategoryAdmin(ShowCaseAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        BotConfigs.objects.set_config_value(BotConfigsEnum.new_keyboard_exists, True)
