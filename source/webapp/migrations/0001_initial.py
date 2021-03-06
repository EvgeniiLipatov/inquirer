# Generated by Django 2.2 on 2019-11-16 06:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Товар')),
                ('category', models.CharField(choices=[('other', 'Другое'), ('food', 'Еда'), ('clothes', 'Одежда'), ('household', 'Товары для дома')], default='other', max_length=50, verbose_name='Категория')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='product_images', verbose_name='Фото')),
                ('description', models.TextField(blank=True, max_length=1000, null=True, verbose_name='описание')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=1000, verbose_name='Текст отзыва')),
                ('mark', models.IntegerField(choices=[('terrible', 1), ('bad', 2), ('satisfied', 3), ('good', 4), ('excellent', 5)], default=3, verbose_name='Категория')),
                ('author', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('good', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='goods', to='webapp.Product', verbose_name='Код товара')),
            ],
        ),
    ]
