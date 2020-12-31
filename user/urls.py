from django.urls import path
from .views import UserSignUp, UserSignin, UserSignOut, UserProfile, UserEditProfile, OthersProfileView

urlpatterns = [
    path("signup/", UserSignUp.as_view()),
    path("login/", UserSignin.as_view()),
    path("logout/", UserSignOut.as_view()),
    path("profile/", UserProfile.as_view()),
    path("profile/edit", UserEditProfile.as_view()),
    path("user/<str:username>", OthersProfileView.as_view())
]
