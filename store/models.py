from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
 
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return str(self.user)
    
class Product(models.Model):
    name= models.CharField(max_length=200)
    price= models.DecimalField(max_digits=5, decimal_places=2)
    digital=models.BooleanField(default=False)
    image= models.ImageField(null =True, blank=True)

    def __str__(self):
        return self.name
    

    @property
    def image_url(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url
    

class Order(models.Model):
    customer= models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered =models.DateTimeField(auto_now_add=True)
    complete= models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=200, null=True, blank=True)


    @property
    def shipping(self):
        shipping =False
        orderitem = self.orderitem_set.all()
        
        for order in orderitem:
            if order.product.digital == False:
                shipping = True
        return shipping
 
    # @property
    # def total_cart_price(self):
    #     oderitem = self.orderitem_set.all()
    #     total =  sum([item.cart_total for item in oderitem])
    #     return total
    

    # @property
    # def total_cart_item(self):
    #     orderitem = self.orderitem_set.all()
    #     total = sum([item.quantity for item in orderitem])
    #     return total

    @property
    def total_cart_price(self):
        orderitem = self.orderitem_set.all()
        total =  sum([item.cart_total for item in orderitem])
        return total
    
    @property
    def total_cart_item(self):
        orderitem = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitem])
        return total



class OrderItem(models.Model):
    product= models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity= models.IntegerField(default=1)
    date_added= models.DateTimeField(auto_now_add=True)


    # @property
    # def cart_total(self):
    #     carttotal = self.product.price * self.quantity

    #     return carttotal
    


    @property 
    def cart_total(self):
        total = self.product.price * self.quantity

        return total


   


class ShippingAddress(models.Model):
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE)
    order=models.ForeignKey(Order, on_delete=models.CASCADE)
    address=models.CharField(max_length=200)
    city=models.CharField(max_length=200)
    state=models.CharField(max_length=200)
    zipcode=models.CharField(max_length=200)
    date_added=models.DateTimeField(auto_now_add=True)