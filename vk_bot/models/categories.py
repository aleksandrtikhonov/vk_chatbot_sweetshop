from __future__ import annotations

from django.db.models import QuerySet, Model, CharField, BooleanField


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
