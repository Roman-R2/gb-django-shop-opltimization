from django.db import models


class Category(models.Model):
    name = models.CharField(
        max_length=64,
        unique=True,
        verbose_name='Название'
    )
    slug = models.SlugField(max_length=255, verbose_name='Url', unique=True)
    description = models.TextField(verbose_name='Описание')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория(ю)'
        verbose_name_plural = 'Категории'
        db_table = 'category'

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, verbose_name='Название')
    slug = models.SlugField(max_length=50, verbose_name='Url', unique=True)
    image = models.ImageField(upload_to='products/', blank=True)
    short_desc = models.CharField(max_length=255, blank=True)
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name='Цена'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Опубликовано',
        null=True
    )
    quantity = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='Количество'
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} ({self.category})'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        db_table = 'product'
