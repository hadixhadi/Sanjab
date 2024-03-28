from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser , IsAuthenticated
from courses.models import UserCourse
from dashboard.serializers.admin_serializer import RegisteredCoursesSerializer,\
    UserIdentifierSerializer,AdminUpdateUserSerializer, CreateEmployerUserSerializer ,SimpleStaticSerializer
from rest_framework.response import Response
from rest_framework import status
from dashboard.serializers.front_serializer import UserSerializer
from dashboard.permissions.admin_permissions import IsSuperAdminUser
from dashboard.models import SimpleStattic
from rest_framework import generics
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
        if request.user.is_super_admin == True:
            all_users = get_user_model().objects.all()
        else:
            all_users=get_user_model().objects.filter(is_admin=False)
        ser_data=UserIdentifierSerializer(instance=all_users,many=True)
        return Response(ser_data.data,status=status.HTTP_200_OK)


# class ShowUsers(generics.GenericAPIView):
#     permission_classes = [IsAdminUser]
#     serializer_class = UserIdentifierSerializer
#
#     def get_queryset(self):
#         if self.request.user.is_super_admin == True:
#             all_users = get_user_model().objects.all()
#         else:
#             all_users=get_user_model().objects.filter(is_admin=False)
#         return all_users
#
#     def list(self, request, *args, **kwargs):
#         queryset=self.get_queryset()
#         serializer_data=self.get_serializer(queryset,many=True)
#         return Response(serializer_data.data,status=status.HTTP_200_OK)



class ShowDetailsUsers(APIView):
    permission_classes = [IsAdminUser]
    def get(self,request,national_code):
        user=get_user_model().objects.get(national_code=national_code)
        ser_data=UserSerializer(instance=user)
        return Response(ser_data.data,status=status.HTTP_200_OK)


    def put(self,request,national_code):
        user=get_user_model().objects.get(national_code=national_code)
        ser_data=AdminUpdateUserSerializer(instance=user,data=request.data,partial=True,
                                           context={'request_data':request.data})
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data,status=status.HTTP_200_OK)
        return Response(ser_data.errors,status=status.HTTP_400_BAD_REQUEST)
# class AdminDeleteUser(APIView):
#     permission_classes = [IsAdminUser]
#     def get(self,request,national_code):
#         user=get_user_model().objects.get(national_code=national_code)
#         user.delete()
#         return Response("user deleted successfully",status=status.HTTP_200_OK)



class CreateEmployerUser(APIView):
    permission_classes = [IsAdminUser,IsSuperAdminUser]
    def post(self,request):
        ser_data=CreateEmployerUserSerializer(data=request.data)
        if ser_data.is_valid():
            employer=get_user_model().objects.create(**ser_data.validated_data)
            employer.is_admin=True
            employer.is_active=True
            employer.phone_active=True
            employer.type=3
            employer.save()
            return Response("created successfully",status=status.HTTP_201_CREATED)
        return Response(ser_data.errors,status=status.HTTP_400_BAD_REQUEST)



class ShowStatics(APIView):
    permission_classes = [IsAdminUser]
    def get(self,request):
        simple_statics=SimpleStattic.objects.all()
        ser_data=SimpleStaticSerializer(instance=simple_statics,many=True)
        return Response(ser_data.data,status=status.HTTP_200_OK)