from courses.models import *
from rest_framework import views
from rest_framework.permissions import AllowAny
from courses.serializers.front_serializer import *
from rest_framework.response import Response
# Create your views here.

class CourseView(views.APIView):
    permission_classes = [AllowAny]
    def get(self,request):
        courses=Course.objects.all()
        ser_data=CourseModelSerializer(instance=courses,many=True)
        return Response(ser_data.data)