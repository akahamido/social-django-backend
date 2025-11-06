from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework.validators import UniqueValidator

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "username", "phone", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            identifier=data.get("identifier"), password=data.get("password")
        )
        if not user:
            raise serializers.ValidationError("اطلاعات ورود اشتباه است")
        data["user"] = user
        return data

class ForgotPasswordSerializer(serializers.Serializer):
    identifier = serializers.CharField()

    def validate_identifier(self, value):
        identifier = value.strip()
        if "@" in identifier and "." in identifier.split("@")[-1]:
            return {"type": "email", "value": identifier}
        if identifier.isdigit() and 11 <= len(identifier) <= 13:
            return {"type": "phone", "value": identifier}
        raise serializers.ValidationError("لطفاً ایمیل یا شماره تلفن وارد کنید (username قابل قبول نیست).")

class ResetPasswordSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    otp = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate_identifier(self, value):
        identifier = value.strip()
        if "@" in identifier and "." in identifier.split("@")[-1]:
            return {"type": "email", "value": identifier}
        if identifier.isdigit() and 11 <= len(identifier) <= 13:
            return {"type": "phone", "value": identifier}
        raise serializers.ValidationError("لطفاً ایمیل یا شماره تلفن وارد کنید (username قابل قبول نیست).")

    def validate_otp(self, value):
        if value != "123456":
            raise serializers.ValidationError("OTP نامعتبر است.")
        return value

    def validate_new_password(self, value):
        if not value or len(value) < 6:
            raise serializers.ValidationError("رمز عبور باید حداقل ۶ کاراکتر باشد.")
        return value

    def save(self):
        ident = self.validated_data["identifier"]
        if isinstance(ident, dict):
            ident_type = ident["type"]
            ident_value = ident["value"]
        else:
            ident_type = "email" if ("@" in ident and "." in ident.split("@")[-1]) else "phone"
            ident_value = ident

        if ident_type == "email":
            user = User.objects.filter(email__iexact=ident_value).first()
        else:
            user = User.objects.filter(phone__iexact=ident_value).first()

        if not user:
            raise serializers.ValidationError("کاربری با مشخصات وارد شده یافت نشد.")

        user.set_password(self.validated_data["new_password"])
        user.save()
        return user
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = self.context['request'].user
        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')

        if not user.check_password(old_password):
            raise serializers.ValidationError({"old_password": "رمز عبور فعلی اشتباه است."})

        if old_password == new_password:
            raise serializers.ValidationError({"new_password": "رمز جدید نباید با رمز قبلی یکسان باشد."})

        if len(new_password) < 6:
            raise serializers.ValidationError({"new_password": "رمز عبور باید حداقل ۶ کاراکتر باشد."})

        return attrs

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "username", "email", "phone", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ["username", "email", "phone"]:
            field = self.fields.get(field_name)
            if field and hasattr(field, "validators"):
                field.validators = [v for v in field.validators if not isinstance(v, UniqueValidator)]

    def validate_username(self, value):
        user = self.context['request'].user
        if value and User.objects.exclude(id=user.id).filter(username=value).exists():
            raise serializers.ValidationError("یوزرنیم قبلاً استفاده شده")
        return value

    def validate_email(self, value):
        user = self.context['request'].user
        if value and User.objects.exclude(id=user.id).filter(email=value).exists():
            raise serializers.ValidationError("ایمیل قبلاً استفاده شده")
        return value

    def validate_phone(self, value):
        user = self.context['request'].user
        if value and User.objects.exclude(id=user.id).filter(phone=value).exists():
            raise serializers.ValidationError("شماره تلفن قبلاً استفاده شده")
        return value
