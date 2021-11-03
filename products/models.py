from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.safestring import mark_safe


# Create your models here.
class CategoryModel(models.Model):
    uuid = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'categories'
        verbose_name = 'Categories'
        verbose_name_plural = 'Categories'


class ProductsModel(models.Model):
    uuid = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='image/')
    description = models.TextField()
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE, related_name='product_category')
    price = models.IntegerField()
    discount = models.IntegerField(default=0,
                                   validators=[
                                       MaxValueValidator(100),
                                       MinValueValidator(1)
                                   ])
    offer = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'products'
        verbose_name = 'Products'
        verbose_name_plural = 'Products'

    @property
    def image_preview(self):
        if self.image:
            return mark_safe('<img src="{}" width="150"/>'.format(self.image.url))
        return ""
