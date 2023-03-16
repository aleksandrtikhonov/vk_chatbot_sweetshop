import json

from django.conf import settings
from django.contrib.admin import ModelAdmin, register

from .models import Products, ProductsCategory


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
        with open(settings.KEYBOARD_STATUS_FILE_PATH, 'r+') as file:
            config = json.load(file)
            config["status"] = False
            file.seek(0)
            file.truncate()
            json.dump(config, file, indent=2)
