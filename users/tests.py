from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase,APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Post, Comment


User = get_user_model()

class AuthTests(APITestCase):
    def test_register_user(self):
        url = reverse('register')
        data = {"email": "test@example.com", "password": "123456"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="test@example.com").exists())

    def test_login_user(self):
        user = User.objects.create_user(email="test2@example.com", password="123456")
        url = reverse('login')
        data = {"identifier": "test2@example.com", "password": "123456"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.data)

    def test_forgot_password_with_email_success(self):
        user = User.objects.create_user(email="forgot@example.com", password="abc12345")
        url = reverse('forgot-password')
        data = {"identifier": "forgot@example.com"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("کد OTP", response.data.get("message", "") or response.data.get("detail", ""))

    def test_forgot_password_with_username_not_allowed(self):
        user = User.objects.create_user(username="myuser", email=None, password="abc12345")
        url = reverse('forgot-password')
        data = {"identifier": "myuser"}  
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("لطفاً ایمیل یا شماره تلفن", str(response.data))

    def test_reset_password_success_with_correct_otp(self):
        user = User.objects.create_user(email="reset@example.com", password="oldpass123")
        url = reverse('reset-password')
        data = {"identifier": "reset@example.com", "otp": "123456", "new_password": "newpass456"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        login_url = reverse('login')
        login_data = {"identifier": "reset@example.com", "password": "newpass456"}
        login_resp = self.client.post(login_url, login_data)
        self.assertEqual(login_resp.status_code, status.HTTP_200_OK)

    def test_reset_password_fails_with_wrong_otp(self):
        user = User.objects.create_user(email="reset2@example.com", password="oldpass123")
        url = reverse('reset-password')
        data = {"identifier": "reset2@example.com", "otp": "000000", "new_password": "newpass456"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("OTP نامعتبر است", str(response.data))



    def test_change_password_success(self):
        user = User.objects.create_user(email="chp@example.com", password="oldpass123")
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        url = reverse('change-password')
        data = {"old_password": "oldpass123", "new_password": "newpass456"}
        response = self.client.post(url, data, HTTP_AUTHORIZATION=f"Bearer {access}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("رمز عبور با موفقیت", response.data["message"])

        login_url = reverse('login')
        login_data = {"identifier": "chp@example.com", "password": "newpass456"}
        login_resp = self.client.post(login_url, login_data)
        self.assertEqual(login_resp.status_code, status.HTTP_200_OK)

    def test_change_password_wrong_old(self):
        user = User.objects.create_user(email="wrongold@example.com", password="oldpass123")
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        url = reverse('change-password')
        data = {"old_password": "wrongpass", "new_password": "newpass456"}
        response = self.client.post(url, data, HTTP_AUTHORIZATION=f"Bearer {access}")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("رمز عبور فعلی اشتباه", str(response.data))


    def test_get_profile_requires_auth(self):
        url = reverse('user-me')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_profile_success(self):
        user = User.objects.create_user(email="me@example.com", password="pass12345", first_name="Old", last_name="Name")
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        url = reverse('user-me')
        resp = self.client.get(url, HTTP_AUTHORIZATION=f"Bearer {access}")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data.get("email"), "me@example.com")
        self.assertEqual(resp.data.get("first_name"), "Old")

    def test_patch_partial_update_first_name_only(self):
        user = User.objects.create_user(email="patch@example.com", password="pass12345", first_name="A", last_name="B")
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        url = reverse('user-me')
        data = {"first_name": "NewName"}
        resp = self.client.patch(url, data, content_type='application/json', HTTP_AUTHORIZATION=f"Bearer {access}")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data.get("first_name"), "NewName")
        self.assertEqual(resp.data.get("last_name"), "B")

    def test_patch_username_conflict(self):
        user1 = User.objects.create_user(email="u1@example.com", password="p1", username="existuser")
        user2 = User.objects.create_user(email="u2@example.com", password="p2", username="other")
        refresh = RefreshToken.for_user(user2)
        access = str(refresh.access_token)

        url = reverse('user-me')
        data = {"username": "existuser"}
        resp = self.client.patch(url, data, content_type='application/json', HTTP_AUTHORIZATION=f"Bearer {access}")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("یوزرنیم قبلاً استفاده شده", str(resp.data))

class PostCommentTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='amin', password='123456')
        self.client = APIClient()
        # به جای login، با کاربر authenticate می‌کنیم
        self.client.force_authenticate(user=self.user)

    def test_create_post(self):
        url = reverse('post-list-create')
        data = {"content": "اولین پستم"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.first().author, self.user)

    def test_comment_on_post(self):
        post = Post.objects.create(author=self.user, content="پست تستی")
        url = reverse('comment-list-create', kwargs={'post_id': post.id})
        data = {"content": "کامنت تستی"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.first().author, self.user)