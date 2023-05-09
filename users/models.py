from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    tel = models.CharField(max_length=30)
    address = models.TextField()
    
    def __str__(self):
        return f'{self.user.username}'

    class Meta:
        db_table = u'customers'