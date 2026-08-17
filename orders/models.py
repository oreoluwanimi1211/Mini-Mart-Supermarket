from django.db import models
from accounts.models import CustomUser
from store.models import Variation
from store.models import Product
from django.core.validators import MinValueValidator


class Payment(models.Model):
    user              = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    payment_id        = models.CharField(max_length=100)
    payment_method    = models.CharField(max_length=100)
    email             = models.EmailField()
    verified          = models.BooleanField(default=False)
    amount       = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]) # this is the total amount paid
    status            = models.CharField(max_length=100)
    created_at        = models.DateTimeField(auto_now_add=True)
    ref               = models.CharField(max_length=200)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.payment_id


class Order(models.Model):
    STATUS = (
    ('New', 'New'),
    ('Accepted', 'Accepted'),
    ('Completed', 'Completed'),
    ('Pending', 'Pending'),
    ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment,on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=11)
    email = models.EmailField(max_length=50)
    address_line_1 = models.CharField(max_length=50, blank=True)
    address_line_2   = models.CharField(max_length=50, blank=True)
    country  = models.CharField(max_length=50)
    state    = models.CharField(max_length=50)
    city   = models.CharField(max_length=50)
    note  = models.CharField(max_length=100, blank=True)
    order_total = models.FloatField()
    tax  = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    delivery_fee = models.DecimalField(default=0.0, decimal_places=2, max_digits=12)
    ref  = models.CharField(max_length=32, blank=True) # added this latter 
    paid = models.BooleanField(default=False)
    special_instructions = models.TextField(blank=True, null=True)


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
