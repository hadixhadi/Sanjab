from django.db import models
from django.contrib.auth.models import  AbstractBaseUser
# Create your models here.
class User(AbstractBaseUser):
    TYPE=[
        (1,'FATHER'),
        (2,'MOTHER')
    ]
    type=models.CharField(max_length=20,choices=TYPE)
    first_name=models.CharField(max_length=200)
    last_name=models.CharField(max_length=200)
    father_name=models.CharField(max_length=200)
    national_code=models.CharField(max_length=10,unique=True,primary_key=True)
    birth_date=models.DateField()
    education=models.CharField(max_length=200)
    field_study=models.CharField(max_length=200)
    telephone=models.CharField(max_length=11)
    phone_number=models.CharField(max_length=11,unique=True)
    address=models.CharField(max_length=300)
    Regional_Municipality=models.SmallIntegerField()
    job=models.CharField(max_length=200,null=True,blank=True)
    office_address=models.CharField(max_length=200,null=True,blank=True)
    boys=models.SmallIntegerField()
    girls=models.SmallIntegerField()