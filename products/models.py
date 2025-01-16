from django.db import models



class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)
    supplier_id = models.ForeignKey('suppliers.Supplier', on_delete=models.CASCADE)
    low_stock_threshold = models.PositiveIntegerField(default=10)



    def is_low_stock(self):
        return self.quantity < self.low_stock_threshold

    def __str__(self):
        return self.name
