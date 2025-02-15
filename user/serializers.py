from rest_framework import serializers

from core.models import User, UserOrganization
from core.choices import RoleChoices


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "slug",
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
            "phone",
            "gender",
            "address",
            "thana",
            "city",
            "postal_code",
            "country",
            "image",
            "status",
            "date_joined",
        ]
        extra_kwargs = {"password": {"write_only": True, "required": True}}
        read_only_fields = ("status", "date_joined")

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class UserOrganizationSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        queryset=User.objects.filter(), slug_field="slug", many=False
    )
    role = serializers.ChoiceField(choices=RoleChoices)
    date_joined = serializers.DateTimeField(read_only=True)

    class Meta:
        model = UserOrganization
        fields = ["user", "role", "status", "salary", "date_joined"]
        read_only_fields = ["date_joined"]
