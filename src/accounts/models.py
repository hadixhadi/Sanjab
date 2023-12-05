from django.db import models
from django.contrib.auth.models import  AbstractBaseUser
from django.utils import timezone
from datetime import timedelta
from accounts.manager import CustomUserManager
# Create your models here.
class User(AbstractBaseUser):
    TYPE=[
        (1,'FATHER'),
        (2,'MOTHER')
    ]
    #required fields
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    national_code=models.CharField(max_length=10,unique=True,primary_key=True)
    phone_number=models.CharField(max_length=11,unique=True)


    type=models.SmallIntegerField(choices=TYPE,null=True,blank=True)
    father_name=models.CharField(max_length=200,null=True,blank=True)
    birth_date=models.DateField(null=True,blank=True)
    education=models.CharField(max_length=200,null=True,blank=True)
    field_study=models.CharField(max_length=200,null=True,blank=True)
    telephone=models.CharField(max_length=11,null=True,blank=True)
    address=models.CharField(max_length=300,null=True,blank=True)
    Regional_Municipality=models.SmallIntegerField(null=True,blank=True)
    job=models.CharField(max_length=200,null=True,blank=True)
    office_address=models.CharField(max_length=200,null=True,blank=True)
    boys=models.SmallIntegerField(null=True,blank=True)
    girls=models.SmallIntegerField(null=True,blank=True)
    is_active=models.BooleanField(default=False)
    phone_active=models.BooleanField(default=False)
    is_admin=models.BooleanField(default=False)
    USERNAME_FIELD='national_code'
    REQUIRED_FIELDS = ['phone_number','first_name','last_name']
    objects=CustomUserManager()

    def __str__(self):
        return self.national_code

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class ChildUser(models.Model):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    national_code=models.CharField(max_length=100,primary_key=True)
    birth_date=models.DateField()
    grade=models.CharField(max_length=50)
    school_address=models.CharField(max_length=100)
    father=models.ForeignKey(User,on_delete=models.CASCADE
                             ,related_name="father_child")
    mother=models.ForeignKey(User,on_delete=models.CASCADE
                             ,related_name="mother_child")

class OtpCode(models.Model):
    phone_number=models.CharField(max_length=11)
    code=models.PositiveSmallIntegerField()
    created_time=models.DateTimeField(auto_now_add=True)
    expire_at=models.TimeField(null=True,blank=True)
    def set_expire_time(self):
        self.expire_at=timezone.now() + timedelta(minutes=2)
        self.save()
    def __str__(self):
        return f"{self.phone_number} - {self.code} - {self.created_time}"