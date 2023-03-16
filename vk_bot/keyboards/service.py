from dataclasses import dataclass
from typing import Any

from vk_bot.models.categories import ProductsCategory
from vk_bot.models.product import Products
from vk_bot.models.types import ProductId
from vk_bot.types import NextLevel, Button


@dataclass
class PayloadDTO:
    next_level: NextLevel
    product_description: str | None = None
    photo_link: str | None = None

    def get_payload_as_string(self) -> str:
        return (
            f"{{"
            f"\"next_level\": \"{self.next_level}\", "
            f"\"message\": \"{self.product_description}\","
            f"\"photo_link\": \"{self.photo_link}\""
            f"}}"
        )


class ProductsMenuService:
    def build_categories_menu_buttons(self, category: str) -> list[Button]:
        products = Products.objects.select_active_products_by_category_name(category)
        buttons = []
        for product in products:
            payload = PayloadDTO(product.id, product.description, product.vk_photo_id).get_payload_as_string()
            buttons.append({"action": {"type": "text", "label": f"{product.name}", "payload": payload}})
        payload = PayloadDTO("main_menu", "Выбери раздел").get_payload_as_string()
        buttons.append({"action": {"type": "text", "label": "Назад", "payload": payload}})
        return buttons

    def build_categories_menu_screen(self, category: str) -> dict[str, bool | list[Any]]:
        products_menu = {"inline": False, "one_time": False, "buttons": [self.build_categories_menu_buttons(category)]}
        return products_menu

    def build_product_buttons(self, product_id: ProductId) -> list[Button]:
        product = Products.objects.get_product_by_id(product_id)
        payload = PayloadDTO(product.category, "Выберете позицию").get_payload_as_string()
        return [{"action": {"type": "text", "label": "Назад", "payload": payload}}]

    def build_product_screen(self, product_id: ProductId) -> dict[str, bool | list[dict[str, dict[str, str]]]]:
        product_view = {"inline": False, "one_time": False, "buttons": [self.build_product_buttons(product_id)]}
        return product_view

    def build_main_menu_buttons(self, categories: list[ProductsCategory]) -> list[Button]:
        buttons = []
        for category in categories:
            payload = PayloadDTO(category.name, "Выбери раздел").get_payload_as_string()
            buttons.append({"action": {"type": "text", "label": f"{category.name}", "payload": payload}})
        return buttons

    def build_main_menu_screen(self, categories: list[ProductsCategory]) -> dict[str, bool | list[Any]]:
        main_menu = {"inline": False, "one_time": False, "buttons": [self.build_main_menu_buttons(categories)]}
        return main_menu


products_menu_service = ProductsMenuService()
