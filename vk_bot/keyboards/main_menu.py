from vk_bot.keyboards.service import products_menu_service, ProductsMenuService
from vk_bot.models import ProductsCategory, Products


class KeyBoard:
    def __init__(self):
        self.updated = True
        self.categories = ProductsCategory.objects.select_active_product_categories()
        self.products = Products.objects.select_active_products()
        self.service = ProductsMenuService()
        self.menu = {}

    def build_keyboard(self):
        self.menu["main_menu"] = self.service.build_main_menu_screen(self.categories)
        for category in self.categories:
            self.menu[category.name] = self.service.build_categories_menu_screen(category.name)
        for product in self.products:
            self.menu[str(product.id)] = products_menu_service.build_product_screen(product.id)
        return self.menu

    def rebuild_keboard(self):
        self.categories = ProductsCategory.objects.select_active_product_categories()
        self.products = Products.objects.select_active_products()
        self.menu = self.build_keyboard()
        return self.menu

    def is_new(self):
        return self.updated

    def set_new(self, value: bool):
        self.updated = value


key_board_manager = KeyBoard()
