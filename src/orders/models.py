from django.contrib.auth import get_user_model
from django.db import models
from courses.models import Course
from accounts.models import ChildUser
# Create your models here.

class Order(models.Model):
    user=models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name="user_orders")
    paid=models.BooleanField(default=False)
    created=models.DateTimeField(auto_now_add=True)

class OrderItems(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name="order_items")
    child=models.ForeignKey(ChildUser,on_delete=models.CASCADE)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    quantity=models.PositiveSmallIntegerField(default=1)
    price=models.BigIntegerField()
    created=models.DateTimeField()



