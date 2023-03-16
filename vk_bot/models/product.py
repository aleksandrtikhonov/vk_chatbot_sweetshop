from __future__ import annotations

from typing import Self

from django.db.models import Model, ForeignKey, DO_NOTHING, CharField, BooleanField, QuerySet

from vk_bot.models.categories import ProductsCategory
from vk_bot.models.types import ProductId


class ProductsQs(QuerySet):
    def select_active_products_by_category_name(self, category_name: str) -> list[Products]:
        qs: Self = self.filter(category__name=category_name)
        return qs.select_active_products()

    def select_active_products(self) -> Self:
        return self.filter(is_active=True)

    def get_product_by_id(self, product_id: ProductId) -> Products:
        return self.get(id=product_id)


class Products(Model):
    class Meta:
        db_table = 'product'
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        unique_together = ('category', 'name')

    category: ProductsCategory = ForeignKey(ProductsCategory, on_delete=DO_NOTHING)

    name: str = CharField(max_length=255, verbose_name='Название товара')
    is_active: bool = BooleanField(default=True, verbose_name='Товар доступен?')
    description: str = CharField(max_length=255, verbose_name='Описание товара', null=True, default=None)
    vk_photo_id: str = CharField(
        max_length=50,
        verbose_name='Ссылка на фото товара в вк группе',
        help_text='Например: photo-123456_654231',
        null=True,
        default=None,
    )

    objects: ProductsQs[Products] = ProductsQs.as_manager()

    def __str__(self) -> str:
        return self.name
