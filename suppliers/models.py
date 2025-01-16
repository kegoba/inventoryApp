from django.db import models



class Supplier(models.Model):
    first_name = models.CharField(max_length=20,default="")
    last_name = models.CharField(max_length=20, default="")
    email = models.EmailField(max_length=255,unique=True)

    def __str__(self):
        return self.first_name
