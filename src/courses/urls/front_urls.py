from django.urls import path
from courses.views.front_views import *
urlpatterns=[
    path('list/',CourseView.as_view(),name="course-list"),
    path("create/",CreateUserCourseView.as_view(),name="create-course"),
    path('video/<int:course_id>/<int:content_id>/<int:object_id>/',SetVideoDone.as_view())
]