from django.contrib.auth.models import BaseUserManager
from django.db import transaction


class CustomUserManager(BaseUserManager):
    def create_user(self,first_name,last_name,
                    national_code,phone_number,**extra_kwargs):
        if not first_name:
            raise ('first name is requird')
        if not last_name:
            raise ('last name is requird')
        if not national_code:
            raise ('national code is requird')
        if not phone_number:
            raise ('phone number is requird')
        user=self.model(first_name=first_name,
                        last_name=last_name,
                        national_code=national_code,
                        phone_number=phone_number)
        user.set_password(national_code)
        user.save(using=self._db)
        return user 
    def create_superuser(self,first_name,last_name,
                         phone_number,national_code,password=None):
       with transaction.atomic():
           user=self.create_user(first_name=first_name,last_name=last_name,
                             national_code=national_code,phone_number=phone_number)
           user.is_admin=True
           user.is_active = True
           user.save(using=self._db)
           return user
