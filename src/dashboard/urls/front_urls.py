from django.urls import path
from dashboard.views.front_views import *
urlpatterns=[
    path("",EntryDashboardView.as_view(),
         name="dashboard"),

    path("my-courses/",UserCoursesView.as_view(),
         name="user-courses"),

    path("course-modules/<int:id>",UserCourseModules.as_view(),
         name="user-course-modules"),

    path("change-child-user/<int:national_code>/",ChangeChildUserView.as_view(),
         name="change-child-user"),

    path("my-course/<int:course_id>/",ShowCourseContentsView.as_view(),
         name="show-contents"),

    #course_id => UserCourse record id
    path("modify-child/<int:national_code>",ModifyChildView.as_view(),
         name="modify-child"),

    path("child-courses/<int:national_code>",CoursesByChild.as_view(),
         name="courses-by-child"),

    path("child-values/<int:national_code>/",ChildValues.as_view(),
         name="child-values")
]