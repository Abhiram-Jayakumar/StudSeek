from django.db import models

# Create your models here.

class Admintable(models.Model):
    email = models.EmailField(unique=True)
    password=models.CharField(max_length=50)


class District(models.Model):
    District_name=models.CharField(max_length=20)

    def __str__(self):
        return self.District_name


class Place(models.Model):
    District=models.ForeignKey(District,on_delete=models.CASCADE)
    Place_name=models.CharField(max_length=20)
    Pincode=models.CharField(max_length=20)

    def __str__(self):
       return self.Place_name