from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailOrUsernameOrPhoneBackend(BaseBackend):
    def authenticate(self, request, identifier=None, password=None, **kwargs):
        if not identifier or not password:
            return None
        user = None
        for field in ["email", "username", "phone"]:
            try:
                user = User.objects.get(**{f"{field}__iexact": identifier})
                break
            except User.DoesNotExist:
                continue

        if user and user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
