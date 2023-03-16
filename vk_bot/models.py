from __future__ import annotations

from typing import Self, NewType

from django.db.models import (
    BooleanField,
    CharField,
    Model,
    Model,
    QuerySet,
    ForeignKey,
    DO_NOTHING,
)

ProductId = NewType('ProductId', int)


class ProductsCategoryQs(QuerySet):
    def select_active_product_categories(self) -> list[ProductsCategory]:
        return self.filter(is_active=True)


class ProductsCategory(Model):
    class Meta:
        db_table = 'product_category'
        verbose_name = 'Категория товара'
        verbose_name_plural = 'Категории товаров'

    name: str = CharField(max_length=255, verbose_name='Название категории', unique=True)
    is_active: bool = BooleanField(default=True, verbose_name='Категория активна?')

    objects: ProductsCategoryQs[ProductsCategory] = ProductsCategoryQs.as_manager()

    def __str__(self) -> str:
        return self.name


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
