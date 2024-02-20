from django.db import models

# Create your models here.
class SimpleStattic(models.Model):
    TYPE=[
        (1,'ALL VIEWS'),
        (2,'USERS'),
        (3,'REGISTERED COURSE')
    ]
    date=models.DateTimeField(auto_now_add=True)
    views=models.BigIntegerField()
    type=models.PositiveSmallIntegerField(choices=TYPE)