from django.db import models

CURRENCIES = (
    ("EUR", 0),
    ("USD", 1),
)

class Activity(models.Model):
    name = models.CharField(max_length=200)
    currency = models.IntegerField(choices=CURRENCIES)
    goal = models.DecimalField(max_digits=6, decimal_places=2)
    pledge_value = models.DecimalField(max_digits=6, decimal_places=2)
    min_people = models.IntegerField()
    max_people = models.IntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

