from django.db import models

# Create your models here.
class Medicine(models.Model):
    types=(
    ('Syp', 'Syp'), ('Tab', 'Tab'),
    ('Amp', 'Amp'), ('Eff', 'Eff'),
    ('Cream/Oin', 'Cream/Oin'), ('Drop', 'Drop'),
    ('Spray', 'Spray'), ('Supp', 'Supp'),
    ('vial', 'Vial'), ('Else', 'Else'),
    )
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=types)
    barcode = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField(default=0)
    min_stock = models.IntegerField(default=2)

    def __str__(self):
        return f"{self.name} - {self.type}"


class Shortage(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.SET_NULL, null=True, blank=True)
    medicine_name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_ordered = models.BooleanField(default=False)
    reported_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.medicine.name if self.medicine else self.medicine_name
