
from rest_framework import serializers
from accounts.models import Visit
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

MyUser = get_user_model()

class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('id', 'username', 'first_name', 'last_name', 
                  'email', 'phone', 'address', 'birth')

class UserDetailSerializer(UserSerializer):
    visits = VisitSerializer(many=True, read_only=True)
    class Meta:
        model = MyUser
        fields = ('id', 'username', 'first_name', 'last_name', 'is_staff', 
                  'email', 'image', 'phone', 'address', 'birth', 'visits')
        read_only_fields = ('username',)
    
class UserRegistrationSerializer(UserSerializer):
    password = serializers.CharField(min_length=10, write_only=True)
    confirm_password = serializers.CharField(min_length=10, write_only=True)

    class Meta:
        model = MyUser
        fields = ('id', 'username', 'first_name', 'last_name', 
                  'email', 'image', 'password', 'confirm_password', 'phone', 'address', 'birth')
        extra_kwargs = {
            'password': {'required': True},
            'confirm_password': {'required': True},
            'username': {'required': True},
            'phone': {'required': True},
            'address': {'required': True}
        }

    def validate_email(self, email):
        existing = MyUser.objects.filter(email=email).first()
        if existing:
            raise serializers.ValidationError("Someone with that email "
                "address has already registered. Was it you?")
        return email
    
    def validate(self, data):
        if not data.get('password') or not data.get('confirm_password'):
            raise serializers.ValidationError("Please enter a password and confirm it.")
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("Those passwords don't match.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        validated_data['password'] = make_password(validated_data['password'])
        user = MyUser.objects.create(**validated_data)
        return user