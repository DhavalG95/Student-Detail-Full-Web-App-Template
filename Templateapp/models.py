from django.db import models


gender_choices = [
    ("m","male"),
    ("f","female")
]

status_choices= (('Active', 'active'),('Inactive', 'inactive'),)

class Student(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    email = models.EmailField(max_length=50)
    gender = models.CharField(max_length=50,choices=gender_choices,default="male")
    created_by=models.CharField(max_length=50,null=True,blank=True)
    updated_by=models.CharField(max_length=50,null=True,blank=True)
    created_at=models.DateTimeField(null=True,blank=True)
    updated_at= models.DateTimeField(null=True,blank=True)
    status = models.CharField(max_length=30,choices=status_choices,default="active")

    
    def __str__(self):
        return self.name
    
class LoginUser(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.username