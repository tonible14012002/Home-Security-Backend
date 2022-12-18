from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from .serializers import UserSerializer
from django.contrib.auth import authenticate, get_user_model

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['user'] = UserSerializer(self.user).data
        return data

class MyTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        print(attrs)
        # request = self.context.get('request')
        # username_field = get_user_model().USERNAME_FIELD
        # authenticate_kwargs = {
        #     username_field: attrs[username_field],
        #     "password": attrs["password"]
        # }
        # user = authenticate(**authenticate_kwargs)
        # data['user'] = UserSerializer(user).data
        return data
        
        # username_field_name = 
class MyTokenRefreshView(TokenRefreshView):
    serializer_class = MyTokenRefreshSerializer
        
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
