from rest_framework import serializers
from .models import User, UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "username",
            "first_name",
            "last_name",
            "is_active",
            "date_joined",
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["phone", "address", "date_of_birth"]


class UserWithProfileSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "is_active",
            "date_joined",
            "profile",
        ]


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "first_name",
            "last_name",
            "password",
            "password_confirm",
        ]

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError("Password do not match")
        return attrs

    def create(self, validated_data):
        # FIXED PASSWORD SAVING
        validated_data.pop("password_confirm")
        password = validated_data.pop("password")  # пароль хешируется
        user = User.objects.create_user(
            password=password, **validated_data
        )  # пароль прописать явно

        # user.set_password(password)
        # user.save()
        UserProfile.objects.create(user=user)
        return user
