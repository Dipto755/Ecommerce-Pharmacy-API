from rest_framework import serializers

from core.models import Organization, UserOrganization, User
from core.choices import RoleChoices, StatusChoices

from user.serializers import UserSerializer


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = [
            "id",
            "uid",
            "name",
            "email",
            "phone",
            "trade_license",
            "address",
            "thana",
            "city",
            "postal_code",
            "country",
            "logo",
            "description",
            "date_joined",
            "updated_at",
        ]

        read_only_fields = ["id", "uid", "date_joined", "updated_at"]

    def create(self, validated_data):
        organization = Organization.objects.create(**validated_data)
        organization.status = StatusChoices.INACTIVE
        organization.save()
        UserOrganization.objects.create(
            user=self.context["request"].user,
            organization=organization,
            role=RoleChoices.OWNER,
            salary=0,
            status=StatusChoices.INACTIVE,
        )
        return organization


class PublicOrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = [
            "name",
            "email",
            "address",
            "thana",
            "city",
            "postal_code",
            "country",
            "logo",
            "description",
        ]


class UserOrganizationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")

    class Meta:
        model = UserOrganization
        fields = ["id", "uid", "username", "role", "status", "salary"]


class OrganizationInternalDetailsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    organization = serializers.CharField(source="organization.name")

    class Meta:
        model = UserOrganization
        fields = ["id", "uid", "user", "organization", "role", "status", "salary"]


class OrganizationInternalSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    email = serializers.EmailField(source="user.email")
    password = serializers.CharField(source="user.password", write_only=True)
    organization = serializers.CharField()
    role = serializers.ChoiceField(choices=RoleChoices)
    # organization = serializers.CharField()

    class Meta:
        model = UserOrganization
        fields = [
            "id",
            "uid",
            "username",
            "email",
            "password",
            "organization",
            "role",
            "status",
            "salary",
        ]

    def validate_organization(self, data):
        orgs = UserOrganization.objects.IS_ACTIVE().filter(
            user=self.context["request"].user
        ).values_list("organization", flat=True)

        curr_user_organizations = Organization.objects.filter(id__in=orgs)
        org = Organization.objects.get(name=data)
        # print(curr_user_organizations)
        # print(org)
        if org not in curr_user_organizations:
            raise serializers.ValidationError(
                "Organization does not match with your organization"
            )

        return org

    def validate_role(self, data):
        curr_user = UserOrganization.objects.IS_ACTIVE().get(
            user=self.context["request"].user
        )
        curr_user_role = curr_user.role.lower()

        role_dict = {"owner": 1, "admin": 2, "manager": 3, "staff": 4}

        if role_dict[curr_user_role] >= role_dict[data.lower()]:
            raise serializers.ValidationError(
                "You do not have permission to create this role"
            )

        return data

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        username = user_data.get("username")
        email = user_data.get("email")
        password = user_data.get("password")
        user = User.objects.create(username=username, email=email)
        user.set_password(password)
        user.save()

        # if UserOrganization.objects.filter(
        #     user=user, status=StatusChoices.ACTIVE
        # ).exists():
        #     raise serializers.ValidationError("User is already in the organization")

        # org =
        organization_user = UserOrganization.objects.create(user=user, **validated_data)
        return organization_user

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", [])
        # organization = validated_data.pop("organization", [])

        curr_user = UserOrganization.objects.IS_ACTIVE().get(
            user=self.context["request"].user
        )
        curr_user_role = curr_user.role.lower()
        role_dict = {"owner": 1, "admin": 2, "manager": 3, "staff": 4}

        if curr_user.organization != instance.organization:
            raise serializers.ValidationError(
                "You are not authorized to edit this user."
            )

        if role_dict[curr_user_role] >= role_dict[instance.role.lower()]:
            raise serializers.ValidationError(
                "You do not have permission to perform this action"
            )
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if user_data:
            user = instance.user
            user.username = user_data.get("username", user.username)
            user.email = user_data.get("email", user.email)
            user.save()

        return instance


# class OwnerOrganizationUserSerializer(serializers.ModelSerializer):

#     username = serializers.CharField(source='user.username')
#     email = serializers.EmailField(source = 'user.email')
#     # org_name = serializers.CharField(source='organization.name')
#     role = serializers.ChoiceField(choices=OwnerRoleChoices.CHOICES)
#     class Meta:
#         model = UserOrganization
#         fields = ['username', 'email' , 'role', 'status', 'salary']

#     def create(self, validated_data):

#         user_data = validated_data.pop('user')
#         username = user_data.get('username')
#         email = user_data.get('email')

#         user = User.objects.get(username=username, email = email)

#         organization_user = UserOrganization.objects.create(user=user, **validated_data)
#         return organization_user

#     def update(self, instance, validated_data):
#         user_data = validated_data.pop('user', [])

#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
#         instance.save()

#         if user_data:
#             user = instance.user
#             user.username = user_data.get('username', user.username)
#             user.email = user_data.get('email', user.email)
#             user.save()


#         return instance


# class AdminOrganizationUserSerializer(serializers.ModelSerializer):

#     username = serializers.CharField(source='user.username')
#     email = serializers.EmailField(source = 'user.email')
#     role = serializers.ChoiceField(choices=AdminRoleChoices.CHOICES)
#     class Meta:
#         model = UserOrganization
#         fields = ['username', 'email', 'role', 'status', 'salary']

#     def create(self, validated_data):

#         user_data = validated_data.pop('user')
#         username = user_data.get('username')
#         email = user_data.get('email')

#         user= User.objects.get(username=username, email=email)

#         organization_user = UserOrganization.objects.create(user=user, **validated_data)
#         return organization_user

# class ManagerOrganizationUserSerializer(serializers.ModelSerializer):

#     username = serializers.CharField(source='user.username')
#     email = serializers.EmailField(source = 'user.email')
#     role = serializers.ChoiceField(choices=ManagerRoleChoices.CHOICES)
#     class Meta:
#         model = UserOrganization
#         fields = ['username', 'email', 'role', 'status', 'salary']

#     def create(self, validated_data):

#         user_data = validated_data.pop('user')
#         username = user_data.get('username')
#         email = user_data.get('email')


#         user= User.objects.get(username=username, email=email)

#         organization_user = UserOrganization.objects.create(user=user, **validated_data)
#         return organization_user
