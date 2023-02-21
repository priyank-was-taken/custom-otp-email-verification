from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from . import models

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = "__all__"

class UserRegisterserializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password], style={"input_type": "password"})
    password2 = serializers.CharField(write_only=True, required=True, style={"input_type": "password"})
    is_verified = serializers.BooleanField(read_only=True)

    class Meta:
        model = models.User
        fields = ["id", "email", "password", "password2", 'is_verified']

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"error": "password field didn't match"})
        return attrs

    def create(self, validated_data):
        user = models.User.objects.create(email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user

        
class OtpVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()        