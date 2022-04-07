from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class mylist(models.Model):
   user = models.ForeignKey(User,on_delete=models.CASCADE)
   id = models.IntegerField(unique=True,primary_key=True)
   model = models.CharField(max_length=200)
   company = models.CharField(max_length=200)
   year = models.CharField(max_length=200)
   price = models.IntegerField()
   transmission = models.CharField(max_length=200)
   mileage = models.CharField(max_length=200)
   fueltype = models.CharField(max_length=200)
   tax = models.CharField(max_length=200)
   mpg = models.CharField(max_length=200)
   enginesize = models.CharField(max_length=200)

   def __str__(self):
      return self.user.username+'-'+self.model
