from django.db import models
from django.utils.text import slugify
from category.models import Category
from django.urls import reverse
from django.conf import settings
from accounts.models import CustomUser

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
    # user_wishlist = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='user_wishlist', blank=True)

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return str(self.product_name)

class WishList(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='wishlist')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.date_created

class WishListItem(models.Model):
    wishlist = models.ForeignKey(WishList, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField()
    
    class Meta:
        unique_together = ('wishlist', 'product')

    def __str__(self):
        return self.product.product_name
    

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