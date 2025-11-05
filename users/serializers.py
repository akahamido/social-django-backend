from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

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
