from rest_framework import serializers
from accounts.models import User
from accounts.serializers.front_serializer import ChildRegisterSerializer


class EntryDashboardSerializer(serializers.ModelSerializer):
    children=serializers.SerializerMethodField()
    class Meta:
        model=User
        exclude=['password','is_active','phone_active','is_admin']
    def get_children(self,obj):
        childes=obj.father_child.all()
        ser_data=ChildRegisterSerializer(childes,many=True)
        return ser_data.data