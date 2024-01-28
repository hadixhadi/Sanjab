from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from courses.models import UserCourse
from dashboard.serializers.admin_serializer import RegisteredCoursesSerializer,UserIdentifierSerializer
from rest_framework.response import Response
from rest_framework import status
from dashboard.serializers.front_serializer import UserSerializer
class RegisteredCourses(APIView):
    permission_classes = [IsAdminUser]
    def get(self,request):
        user_courses=UserCourse.objects.all()
        ser_data=RegisteredCoursesSerializer(instance=user_courses,many=True)
        return Response(ser_data.data,status=status.HTTP_200_OK)


class EntryAdminDashboard(APIView):
    permission_classes = [IsAdminUser]
    def get(self,request):
        ser_data=UserIdentifierSerializer(instance=request.user)
        return Response(ser_data.data,status=status.HTTP_200_OK)

class ShowUsers(APIView):
    permission_classes = [IsAdminUser]
    def get(self,request):
        all_users=get_user_model().objects.filter(is_admin=False)
        ser_data=UserIdentifierSerializer(instance=all_users,many=True)
        return Response(ser_data.data,status=status.HTTP_200_OK)


class ShowDetailsUsers(APIView):
    permission_classes = [IsAdminUser]
    def get(self,request,national_code):
        user=get_user_model().objects.get(Q(national_code=national_code)& Q(is_admin=False))
        ser_data=UserSerializer(instance=user)
        return Response(ser_data.data,status=status.HTTP_200_OK)