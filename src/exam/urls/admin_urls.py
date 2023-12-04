from django.urls import path
from exam.views.admin_views import ExamsViewsets , QuestionViewsets
urlpatterns=[
    # path('exam-list',ExamsViewsets.as_view({'get':'list'})),
    # path('qs-list',QuestionViewsets.as_view({'get':'list'}))
]