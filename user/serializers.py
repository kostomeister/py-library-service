from django.contrib.auth import get_user_model
from rest_framework import serializers
from secrets import token_urlsafe


class UserSerializer(serializers.ModelSerializer):
    bot_link = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ("id", "email", "password", "is_staff", "bot_link")
        read_only_fields = ("is_staff", "bot_link")
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, set the password correctly and return it"""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()

        return user

    def get_bot_link(self, value) -> str:
        user_token = token_urlsafe(16)
        user_id = self.context['request'].user.id
        bot_name = "BuzzingPagesBot"

        return (f"https://telegram.me/{bot_name}?start={user_token}"
                f"userid{user_id}")
