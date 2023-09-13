from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)
        verbose_name_plural='Categories'

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category,related_name='items',on_delete=models.CASCADE)
    image = models.ImageField(upload_to='item_images',blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    price = models.FloatField()
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add = True)
    created_by = models.ForeignKey(User,related_name='items',on_delete=models.CASCADE)

    def __str__(self):
        return self.name[:10]
