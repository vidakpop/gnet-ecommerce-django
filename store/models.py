from django.db import models
import datetime

#categories of products
class Category(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self):
        return self.name  #returns the name in admin
    
    class Meta:
        verbose_name_plural='categories'
    
# customers
class Customer(models.Model):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    phone=models.CharField(max_length=10)
    email=models.EmailField(max_length=100)
    password=models.CharField(max_length=100)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'



#all of our products
class Product(models.Model):
    name=models.CharField(max_length=50)
    price=models.DecimalField(default=0,decimal_places=2,max_digits=8)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    description=models.CharField(max_length=10000,default='',blank=True,null=True)
    image=models.ImageField(upload_to='uploads/product/')

    #add sale 
    on_sale=models.BooleanField(default=False)
    sale_price=models.DecimalField(default=0,decimal_places=2,max_digits=8)

    def __str__(self):
        return self.name
    
#customer orders
class Order(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    address=models.CharField(max_length=100,default='',blank=True)
    phone=models.CharField(max_length=10,default='',blank=True)
    date=models.DateField(default=datetime.datetime.today)
    status=models.BooleanField(default=False)

    def __str__(self):
        return self.product





