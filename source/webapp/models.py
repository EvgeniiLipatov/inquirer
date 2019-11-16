from django.contrib.auth.models import User
from django.db import models

CATEGORY_CHOICES = (
    ('other', 'Другое'),
    ('food', 'Еда'),
    ('clothes', 'Одежда'),
    ('household', 'Товары для дома'),
)

MARK_CHOICE = (
    ('terrible', 1),
    ('bad', 2),
    ('satisfied', 3),
    ('good', 4),
    ('excellent', 5)
)


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='Товар')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default=CATEGORY_CHOICES[0][0],
                                verbose_name='Категория')
    photo = models.ImageField(upload_to='product_images', null=True, blank=True, verbose_name='Фото')
    description = models.TextField(max_length=1000, null=True, blank=True, verbose_name='описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Review(models.Model):
    good = models.ForeignKey('webapp.Product', related_name='goods',
                                on_delete=models.CASCADE, verbose_name='Код товара')
    text = models.TextField(max_length=1000, verbose_name='Текст отзыва')
    author = models.ForeignKey('auth.User', null=True, blank=True, default=None, verbose_name='Автор',
                               on_delete=models.CASCADE, related_name='reviews')
    mark = models.IntegerField(choices=MARK_CHOICE, default=MARK_CHOICE[2][1],
                                verbose_name='Категория')


    def __str__(self):
        return self.text[:20]

