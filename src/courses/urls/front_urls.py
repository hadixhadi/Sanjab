from django.urls import path
from courses.views.front_views import *
urlpatterns=[
    path('list/',CourseView.as_view(),name="course-list"),


    path("create/",CreateUserCourseView.as_view(),name="create-course"),


    path('content/<int:course_id>/<int:content_id>/<int:object_id>/',SetContentDone.as_view(),
         name="set-content-done")
]