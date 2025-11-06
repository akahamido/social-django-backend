from django.urls import path
from .views import RegisterView, LoginView,ForgotPasswordView,ResetPasswordView,ChangePasswordView,UserMeView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot-password"),
    path("reset-password/", ResetPasswordView.as_view(), name="reset-password"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("me/", UserMeView.as_view(), name="user-me"),


]
