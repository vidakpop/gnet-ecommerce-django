from django.db import models
from django.contrib.auth.models import User
from store.models import Product


# Create order model
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    full_name=models.CharField(max_length=250)
    email=models.EmailField(max_length=250)
    address1=models.CharField(max_length=250)
    address2=models.CharField(max_length=250)
    amount_paid=models.DecimalField(max_digits=25,decimal_places=2)
    date_ordered=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order -{str(self.id)}'

#Create Order Items Model
class OrderItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    order=models.ForeignKey(Order,on_delete=models.CASCADE,null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)

    quantity=models.PositiveBigIntegerField(default=1)
    price=models.DecimalField(max_digits=25,decimal_places=2)

    def __str__(self):
        return f'Order Item -{str(self.id)}'