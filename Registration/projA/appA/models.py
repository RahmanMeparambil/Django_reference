from django.db import models

# Create your models here.

class Registration(models.Model):
    phone= models.CharField(max_length=12,null=True)
    name = models.CharField(max_length=20,null=True)
    address = models.CharField(max_length=255,null=True)
    email = models.EmailField(null=True)
    pincode = models.IntegerField(null=True)
    file = models.FileField(upload_to='files',null=True)

    def __str__(self):
        return self.name