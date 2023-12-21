from django.urls import path
from dashboard.views.front_views import *
urlpatterns=[
    path("",EntryDashboardView.as_view(),name="dashboard"),
    path("my-courses",UserCoursesView.as_view(),name="user-courses"),
    path("course-modules/<int:id>",UserCourseModules.as_view(),name="user-course-modules"),
    path("change-child-user/<int:national_code>",ChangeChildUserView.as_view(),name="change-child-user"),

]