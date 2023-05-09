from django.db import models
from users.models import User, Customer
from store.models import Product

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=500, default='a')
    price = models.FloatField(default=0.0)
    image_product = models.ImageField(upload_to='store/img', default='store/img/img_coming_soon.png')
    quantity = models.PositiveIntegerField(default=0)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.id)