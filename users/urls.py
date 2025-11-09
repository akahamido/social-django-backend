from django.urls import path
from .views import (RegisterView, LoginView,ForgotPasswordView,
                    ResetPasswordView,ChangePasswordView,UserMeView,
                    PostListCreateView, PostRetrieveUpdateDestroyView,
                    CommentListCreateView, CommentRetrieveUpdateDestroyView,
                    ChangeUsernameView)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot-password"),
    path("reset-password/", ResetPasswordView.as_view(), name="reset-password"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("me/", UserMeView.as_view(), name="user-me"),
    path("posts/", PostListCreateView.as_view(), name="post-list-create"),
    path("posts/<uuid:pk>/", PostRetrieveUpdateDestroyView.as_view(), name="post-detail"),
    path("posts/<uuid:post_id>/comments/", CommentListCreateView.as_view(), name="comment-list-create"),
    path("comments/<uuid:pk>/", CommentRetrieveUpdateDestroyView.as_view(), name="comment-detail"),
    path("change-username/", ChangeUsernameView.as_view(), name="change-username"),


]
