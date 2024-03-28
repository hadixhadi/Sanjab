from django.urls import path
from dashboard.views.admin_views import RegisteredCourses, EntryAdminDashboard, \
    ShowUsers, ShowDetailsUsers, CreateEmployerUser, ShowStatics, InactiveUser

urlpatterns=[
    path("",EntryAdminDashboard.as_view(),name='admin-dashboard-entry'),
    path("registered-courses/",RegisteredCourses.as_view(),name='admin-registered-courses'),
    path('users/',ShowUsers.as_view(),name="showusers"),
    path('user/<str:national_code>/',ShowDetailsUsers.as_view()),
    path('create-employer/',CreateEmployerUser.as_view()),
    path('statics',ShowStatics.as_view()),
    path('inactive/<str:national_code>',InactiveUser.as_view(),name="inactive-user")
    # path('user/delete/<str:national_code>/',AdminDeleteUser.as_view())
]