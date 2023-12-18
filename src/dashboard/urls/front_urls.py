from django.urls import path
from dashboard.views.front_views import *
urlpatterns=[
    path("",EntryDashboardView.as_view(),name="dashboard"),
    path("courses",UserCoursesView.as_view(),name="user-courses"),
]