from rest_framework import serializers

from core.models import UserOrganization, User
from core.choices import OwnerRoleChoices, AdminRoleChoices, ManagerRoleChoices, RoleChoices, StatusChoices

from user.serializers import UserSerializer


class UserOrganizationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source = 'user.username')

    class Meta:
        model = UserOrganization
        fields = ['username', 'role', 'status', 'salary']
        

class OrganizationInternalDetailsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserOrganization
        fields = ['user', 'role', 'status', 'salary']


class OrganizationInternalSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    role = serializers.ChoiceField(choices=RoleChoices.CHOICES)
    
    class Meta:
        model = UserOrganization
        fields = ['username', 'email', 'role', 'status', 'salary']
        
    def validate_role(self, data):
        curr_user = UserOrganization.objects.get(user=self.context['request'].user, status = StatusChoices.Active)
        curr_user_role = curr_user.role
        
        role_dict = {
            'owner': 1,
            'admin': 2,
            'manager': 3,
            'staff': 4
        }
        
        if role_dict[curr_user_role] >= role_dict[data]:
            raise serializers.ValidationError('You do not have permission to create this role')
            
        return data
            
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        username = user_data.get('username')
        email = user_data.get('email')
        user = User.objects.get(username=username, email=email)
        
        if UserOrganization.objects.filter(user=user, status=StatusChoices.Active).exists():
            raise serializers.ValidationError('User is already in the organization')
        
        organization_user = UserOrganization.objects.create(user=user, **validated_data)
        return organization_user
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', [])

        curr_user = UserOrganization.objects.get(user=self.context['request'].user, status = StatusChoices.Active)
        curr_user_role = curr_user.role
        role_dict = {
            'owner': 1,
            'admin': 2,
            'manager': 3,
            'staff': 4
        }
        
        if role_dict[curr_user_role] >= role_dict[instance.role]:
            raise serializers.ValidationError('You do not have permission to perform this action')
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if user_data:
            user = instance.user
            user.username = user_data.get('username', user.username)
            user.email = user_data.get('email', user.email)
            user.save()
            
        return instance
        


class OwnerOrganizationUserSerializer(serializers.ModelSerializer):
    
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source = 'user.email')
    # org_name = serializers.CharField(source='organization.name')
    role = serializers.ChoiceField(choices=OwnerRoleChoices.CHOICES)
    class Meta:
        model = UserOrganization
        fields = ['username', 'email' , 'role', 'status', 'salary']

    def create(self, validated_data):

        user_data = validated_data.pop('user')
        username = user_data.get('username')
        email = user_data.get('email')

        user = User.objects.get(username=username, email = email)
                
        organization_user = UserOrganization.objects.create(user=user, **validated_data)
        return organization_user
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if user_data:
            user = instance.user
            user.username = user_data.get('username', user.username)
            user.email = user_data.get('email', user.email)
            user.save()


        return instance
    

class AdminOrganizationUserSerializer(serializers.ModelSerializer):
    
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source = 'user.email')
    role = serializers.ChoiceField(choices=AdminRoleChoices.CHOICES) 
    class Meta:
        model = UserOrganization
        fields = ['username', 'email', 'role', 'status', 'salary']

    def create(self, validated_data):

        user_data = validated_data.pop('user')
        username = user_data.get('username')
        email = user_data.get('email')

        user= User.objects.get(username=username, email=email)
                
        organization_user = UserOrganization.objects.create(user=user, **validated_data)
        return organization_user
    
class ManagerOrganizationUserSerializer(serializers.ModelSerializer):
    
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source = 'user.email')
    role = serializers.ChoiceField(choices=ManagerRoleChoices.CHOICES) 
    class Meta:
        model = UserOrganization
        fields = ['username', 'email', 'role', 'status', 'salary']

    def create(self, validated_data):

        user_data = validated_data.pop('user')
        username = user_data.get('username')
        email = user_data.get('email')


        user= User.objects.get(username=username, email=email)
                
        organization_user = UserOrganization.objects.create(user=user, **validated_data)
        return organization_user
        