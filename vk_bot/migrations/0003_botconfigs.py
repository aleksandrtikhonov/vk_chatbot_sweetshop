# Generated by Django 4.1.7 on 2023-03-16 13:13

from django.db import migrations, models
import enumchoicefield.fields
import vk_bot.models
import vk_bot.models.types


class Migration(migrations.Migration):

    dependencies = [
        ("vk_bot", "0002_products"),
    ]

    operations = [
        migrations.CreateModel(
            name="BotConfigs",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    enumchoicefield.fields.EnumChoiceField(
                        enum_class=vk_bot.models.types.BotConfigsEnum, max_length=19
                    ),
                ),
                ("value", models.BooleanField(default=False)),
            ],
            options={
                "verbose_name": "Конфигурация бота",
                "verbose_name_plural": "Конфигурации бота",
                "db_table": "bot_config",
            },
        ),
    ]