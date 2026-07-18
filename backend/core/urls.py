from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from .views import RegisterView,AnalysisListCreate,me,review_analysis,users
urlpatterns=[path('auth/register/',RegisterView.as_view()),path('auth/token/',TokenObtainPairView.as_view()),path('auth/token/refresh/',TokenRefreshView.as_view()),path('auth/me/',me),path('analyses/',AnalysisListCreate.as_view()),path('analyses/<int:pk>/review/',review_analysis),path('admin/users/',users)]
