from django.urls import path
from dashboard.views.admin_views import RegisteredCourses, EntryAdminDashboard, \
    ShowUsers, ShowDetailsUsers

urlpatterns=[
    path("",EntryAdminDashboard.as_view(),name='admin-dashboard-entry'),
    path("registered-courses/",RegisteredCourses.as_view(),name='admin-registered-courses'),
    path('users/',ShowUsers.as_view(),name="showusers"),
    path('user/<str:national_code>/',ShowDetailsUsers.as_view()),
    # path('user/delete/<str:national_code>/',AdminDeleteUser.as_view())
]