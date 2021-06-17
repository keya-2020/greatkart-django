from django.db.models.deletion import CASCADE
from category.models import Category
from django.db import models
from category.models import Category
from django.urls import reverse

from django.utils.text import slugify

# Create your models here.

class Products(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug         = models.SlugField(max_length=225, unique=True)
    despriction  = models.TextField(max_length=500, blank=True)
    price        = models.IntegerField()
    image        = models.ImageField(upload_to ='photos/products')
    stock        = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category     = models.ForeignKey(Category, on_delete=CASCADE)
    create_date  = models.DateField(auto_now_add=True)
    modified_date= models.DateField(auto_now=True)

    class Meta:
        verbose_name        = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.product_name
    
    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])
    
    def save (self, *args, **kwargs ):
        self.slug = slugify(self.product_name)
        super().save(*args , **kwargs)


