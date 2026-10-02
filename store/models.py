from django.db import models
from django.utils.text import slugify
from category.models import Category
from django.urls import reverse


# Size
# Color
# Fit
# Length
# Material
# Pattern
# Sleeve
# Neckline
# Waist
# Rise
# Closure
# Pocket
# Hood
# Cuff
# Collar
# Thickness
# Stretch
# Occasion
# Season
# Gender
# Brand
# Clothing Type
# Shoe Variations
# Accessory Variation

class Product(models.Model):
    product_name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    image = models.ImageField(upload_to='photo/products', default='product.jpg')
    stock = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modifield_date = models.DateTimeField(auto_now=True)


    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])


    def __str__(self):
        return str(self.product_name)

class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)
    
    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)

Variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),

)

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=Variation_category_choice)
    is_active = models.BooleanField(default=True)
    variation_value = models.CharField(max_length=100, )
    created_date = models.DateTimeField(auto_now=True)
    time_added = models.TimeField(auto_now_add=True)

    objects = VariationManager()

    def __str__(self):
        return str(self.variation_value)