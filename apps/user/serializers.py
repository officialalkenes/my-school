from datetime import timedelta

from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions

from django.db import IntegrityError, transaction

from django.utils import timezone

from rest_framework import exceptions, serializers
from rest_framework.exceptions import ValidationError
from rest_framework.settings import api_settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from djoser.serializers import UserCreateSerializer


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ""


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password")

    def validate(self, data):
        if len(data["password"]) < 8:
            raise serializers.ValidationError(
                {"details": "Password length Has to be 8 chars long or more"}
            )
        # if data["password"]:
        #     raise serializers.ValidationError({"details": "Please Provide Password"})
        # if len(data["password"]) < 8:
        #     raise serializers.ValidationError({"details": "Please Provide Password"})
        return data


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token["username"] = user.username
        return token


# class LoginUserSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField(
#         style={"input_type": "password"}, trim_whitespace=False
#     )

# def validate(self, attrs):
#     username = attrs.get("username")
#     password = attrs.get("password")
#     now = timezone.now()

# if username and password:
#     try:
#         user = User.objects.filter(username=username).first()
#         login_attempt, created = LoginAttempt.objects.get_or_create(user=user)
#         if (
#             login_attempt.timestamp
#             + timedelta(seconds=settings.LOGIN_ATTEMPTS_TIME_LIMIT)
#         ) < now:
#             user = authenticate(
#                 request=self.context.get("request"),
#                 username=username,
#                 password=password,
#             )

#         else:
#             msg = {"detail": "Error Please Try Again.", "register": False}
#             raise serializers.ValidationError(msg)
#     except User.DoesNotExist or School.DoesNotExist:
#         pass
# else:
#     msg = 'Must include "username" and "password".'
#     raise serializers.ValidationError(msg, code="authorization")

# attrs["user"] = user
# return attrs


class ChangePasswordSerializer(serializers.HyperlinkedModelSerializer):
    old_password = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(
        write_only=True, required=True, trim_whitespace=False
    )

    class Meta:
        model = User
        fields = ("old_password", "password")

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                {"old_password": "Old password is not correct"}
            )
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data["password"])
        instance.save()

        return instance


class PasswordChangeSerializer(serializers.ModelSerializer):
    pass


# class UserSerializer(serializers.ModelSerializer):
#     snippets = serializers.PrimaryKeyRelatedField(
#         many=True, queryset=User.objects.all()
#     )

#     class Meta:
#         model = User
#         fields = ["id", "username", "snippets"]


class AuthenticationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password")


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ["id", "email", "password"]


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    admission_id = serializers.CharField(required=False)
    password = serializers.CharField(style={"input_type": "password"}, required=False)
    id_token = serializers.CharField(required=False)

    def validate(self, data):
        email = data.get("email")
        # password = data.get("password")
        admission_id = data.get("admission_id")
        id_token = data.get("id_token")

        if not email and not admission_id and not id_token:
            raise serializers.ValidationError(
                "Must provide either email and password, admission ID and password, or ID token"
            )
        return data
