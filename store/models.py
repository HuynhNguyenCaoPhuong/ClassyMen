from django.db import models
from django.template.defaultfilters import slugify
from users.models import User
from ckeditor.fields import RichTextField


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(null=True, blank=True)
    sub = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name
    

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category,self).save(*args, **kwargs)


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    img = models.ImageField(upload_to='store/img', default='store/img/img_coming_soon.png')
    slug = models.SlugField(null=True, blank=True)
    size = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.name
    

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(SubCategory,self).save(*args, **kwargs)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=500)
    price = models.FloatField(default=0.0)
    price_origin = models.FloatField(null=True)
    image_product = models.ImageField(upload_to='store/img', default='store/img/img_coming_soon.png')
    describe = RichTextField(null=True, blank=True)
    public_day = models.DateTimeField(auto_now_add=True)
    viewed = models.IntegerField(default=0)
    color = models.CharField(max_length=20, null=True, blank=True)
    size = models.CharField(max_length=20, null=True, blank=True)
    vote = models.FloatField(null=True, blank=True, default=5)
    star = models.TextField(default='<small class="fa fa-star text-primary mr-1"></small><small class="fa fa-star text-primary mr-1"></small><small class="fa fa-star text-primary mr-1"></small><small class="fa fa-star text-primary mr-1"></small><small class="fa fa-star text-primary mr-1"></small>')

    def __str__(self):
        return self.name
    
    def to_dict(self):
        return {
            'name': self.name,
            'describe': self.describe,
            'price': str(self.price), 
        }

    class Meta:
        ordering = ('-public_day',)


class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name_product = models.CharField(max_length=500, default='')
    name = models.CharField(max_length=500)
    img = models.ImageField(upload_to='store/img', default='store/img/img_coming_soon.png', null=True, blank=True)

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=50, null=True, blank=True)
    message = models.TextField()

    def __str__(self):
        return self.name
    
