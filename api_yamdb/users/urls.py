from django.urls import path

from .views import (SelfUserView, UsernameView, UserSignupView, UsersView,
                    VerifyCodeTokenObtainPairView)

urlpatterns = [
    path('auth/signup/', UserSignupView.as_view()),
    path('auth/token/', VerifyCodeTokenObtainPairView.as_view()),
    path('users/me/', SelfUserView.as_view()),
    path('users/<str:username>/', UsernameView.as_view()),
    path('users/', UsersView.as_view()),
]
