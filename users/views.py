from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer, ForgotPasswordSerializer, ResetPasswordSerializer,ChangePasswordSerializer,UserSerializer,PostSerializer, CommentSerializer, ChangeUsernameSerializer
from django.contrib.auth import get_user_model
from .models import Post, Comment, UsernameChangeHistory
from drf_spectacular.utils import extend_schema




User = get_user_model()

@extend_schema(
    operation_id="register_user",
    description="ثبت‌نام کاربر جدید با استفاده از ایمیل، شماره‌تلفن یا یوزرنیم",
    request=RegisterSerializer,
    responses={201: "ثبت‌نام موفق"})

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "ثبت‌نام موفق", "user_id": user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





@extend_schema(
    operation_id="login_user",
    description="ورود کاربر با ایمیل، یوزرنیم یا شماره‌تلفن و دریافت JWT Token",
    request=LoginSerializer,
    responses={200: "ورود موفق، شامل access_token و refresh_token"})

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "access_token": str(refresh.access_token),
                    "refresh_token": str(refresh),
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "username": user.username,
                        "phone": user.phone,
                    },
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



@extend_schema(
    operation_id="forgot_password",
    description="درخواست بازیابی رمز عبور با ارسال ایمیل یا شماره تلفن (OTP فعلاً 123456)",
    request=ForgotPasswordSerializer,
    responses={200: "کد OTP ارسال شد"})


class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            ident = serializer.validated_data["identifier"]
            ident_type = ident["type"]
            ident_value = ident["value"]

            if ident_type == "email":
                user = User.objects.filter(email__iexact=ident_value).first()
            else:
                user = User.objects.filter(phone__iexact=ident_value).first()

            if user:
                return Response({"message": "کد OTP ارسال شد (فعلاً هاردکد: 123456)"},
                                status=status.HTTP_200_OK)
            return Response({"detail": "کاربری با این ایمیل/شماره یافت نشد."},
                            status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






@extend_schema(
    operation_id="reset_password",
    description="تغییر رمز عبور با وارد کردن OTP (فعلاً هاردکد 123456)",
    request=ResetPasswordSerializer,
    responses={200: "رمز عبور با موفقیت تغییر یافت"})

class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
            except Exception as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"message": "رمز عبور با موفقیت تغییر یافت."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    






@extend_schema(
    operation_id="change_password",
    description="تغییر رمز عبور برای کاربر واردشده (با اعتبارسنجی رمز فعلی)",
    request=ChangePasswordSerializer,
    responses={200: "رمز عبور با موفقیت تغییر یافت"})

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "رمز عبور با موفقیت تغییر یافت."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(
    operation_id="get_or_update_profile",
    description="دریافت یا بروزرسانی اطلاعات پروفایل کاربر واردشده (partial update)",
    request=UserSerializer,
    responses={200: UserSerializer})

class UserMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        serializer = UserSerializer(instance=request.user, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



@extend_schema(
    operation_id="create_post",
    description="ایجاد یک پست جدید (می‌تواند شامل mentions باشد)",
    request=PostSerializer,
    responses={201: PostSerializer})

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()



@extend_schema(
    operation_id="retrieve_update_delete_post",
    description="دریافت، بروزرسانی یا حذف یک پست خاص بر اساس post_id",
    request=PostSerializer,
    responses={200: PostSerializer})

class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]




@extend_schema(
    operation_id="create_comment",
    description="ثبت کامنت برای یک پست مشخص (post_id در URL)",
    request=CommentSerializer,
    responses={201: CommentSerializer})

class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post_id=post_id).order_by('-created_at')

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        serializer.save(post_id=post_id, author=self.request.user)




@extend_schema(
    operation_id="retrieve_update_delete_comment",
    description="دریافت، بروزرسانی یا حذف یک کامنت خاص بر اساس comment_id",
    request=CommentSerializer,
    responses={200: CommentSerializer})

class CommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]




@extend_schema(
    operation_id="change_username",
    description="تغییر نام کاربری کاربر و ذخیره در جدول تاریخچه تغییرات",
    request=ChangeUsernameSerializer,
    responses={200: "نام کاربری با موفقیت تغییر یافت"})
class ChangeUsernameView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangeUsernameSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            old = user.username
            user.username = serializer.validated_data['username']
            user.save()
            UsernameChangeHistory.objects.create(
                user=user, old_username=old, new_username=user.username
            )
            return Response({"message": "یوزرنیم با موفقیت تغییر یافت", "username": user.username})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)