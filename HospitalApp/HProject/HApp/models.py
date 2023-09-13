from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
import datetime

# Create your models here.
class Doctor(models.Model):
    Name = models.CharField(max_length=200,null=True)
    Email = models.EmailField(null=True)
    Specialization = models.ForeignKey('Specialization',on_delete=models.CASCADE,null=True)
    Class = models.CharField(max_length = 10 , null = True)
    # Fb_link = models.CharField(max_length=200)
    # In_link = models.CharField(max_length=200)
    # Instagram_link = models.CharField(max_length=200)
    # Twitter_link = models.CharField(max_length=200)
    Image = models.ImageField(upload_to='doctors',null=True)




class Appointment(models.Model):
    Appointment_date = models.DateField(null =True)
    Patient_name = models.CharField(max_length=200,null=True)
    Patient_email = models.EmailField(max_length=200,null=True)
    Specialization = models.CharField(max_length=200,null=True)
    Start_time = models.TimeField(null = True)
    End_time = models.TimeField(null = True)
    Status = models.BooleanField(default=False)
    Doctor_reg = models.ForeignKey(Doctor,on_delete=models.SET_NULL, null=True)
 
    def __str__(self):
        return self.Patient_name
    


# class Blogs(models.Model):
#     Name = models.CharField(max_length=200)
#     Blog_content = models.TextField()
#     Image = models.ImageField()
#     Date_blog = models.DateField()
#     Approval_status = models.CharField(max_length=200)


class Requests(models.Model):
    Name = models.CharField(max_length=200,null=True)
    Email = models.EmailField(null=True)
    User_category = models.CharField(max_length=200,null=True)
    Old_password = models.CharField(max_length=200,null=True)
    New_password = models.CharField(max_length=200,null=True)
    Req_reg = models.ForeignKey(User, on_delete=models.SET_NULL, null = True)
    

class Specialization(models.Model):
    Specialization_name = models.CharField(max_length=200,null=True)
    Description = models.TextField(null=True)
    Icon = models.TextField(null=True)
    Image = models.ImageField(null=True)


class Slot(models.Model):
    Doctor_reg = models.ForeignKey(Doctor, on_delete=models.CASCADE,null=True)
    Date = models.DateField(null=True)
    Start_time = models.TimeField(null=True)
    End_time = models.TimeField(null=True)  
    Is_available = models.BooleanField(default=True)


class Receipt(models.Model):
    Email = models.EmailField(null=True)
    Name = models.CharField(max_length=50,null=True)
    Date = models.DateField(auto_now_add = True)
    Amount = models.FloatField()
    Doctor_reg = models.ForeignKey(Doctor,on_delete=models.CASCADE,null = True)


class Message(models.Model):
    Sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    Recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    Content = models.TextField()
    Is_read = models.BooleanField(default=False)
    Timestamp = models.DateTimeField(auto_now_add=True)

    