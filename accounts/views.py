from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import (
    viewsets,
    generics,
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import (
    SearchFilter, 
    OrderingFilter
)
from .serializers import (
    UserDetailSerializer,
    UserRegistrationSerializer,
    UserSerializer,
    VisitSerializer
)
from .models import MyUser, Visit
from.ultils import detect_face
from .ultils import IsAdminOrAccountOwner
from django.db.models import Count
from rest_framework.decorators import (
    api_view,
    permission_classes
)
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.core.mail import send_mail
from home_security.settings import EMAIL_HOST_USER
import jwt
from rest_framework import status
from django.conf import settings

# Create your views here.

@api_view(['POST'])
def detect_face_by_img(request):
    # try:
        upload_image = request.FILES.get('image')
        user = detect_face(upload_image)

        if len(user) == 1:
            return Response({
                'status': 'success',
                'username': user[0].username
            })

        return Response({
            'status': 'error',
            'message': 'cant detect face'
        })

class OrdinaryUserViewSet(viewsets.ModelViewSet):
    
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ['username', 'first_name', 'email', 'phone', 'address']
    ordering_fields = ['username', 'first_name', 'email', 'phone', 
                       'address', 'visits__time', 'visits']
    
    # def get_permissions(self):
    #     if not self.action == 'create':
    #         return (IsAdminOrAccountOwner(),) 
    #     return []
    
    def get_queryset(self):
        users = MyUser.is_ordinary.all()

        status = self.request.query_params.get('status')
        if status:
            if status == 'accepted':
                users = users.filter(is_accepted=True)
            else:
                users = users.filter(is_accepted=False)

        ordering_choices = self.request.query_params.get('ordering')
        if ordering_choices and 'total_visits' in ordering_choices.split(','):
            if '-total_visits' in ordering_choices.split(','):
                users= users.annotate(total_visits=Count('visits')).order_by('-total_visits')
                return users
            users = users.annotate(total_visits=Count('visits')).order_by('total_visits')
        return users

    def get_serializer_class(self):
        if self.action == 'list':
            return UserSerializer
        if self.action == 'create':
            return UserRegistrationSerializer
        return UserDetailSerializer
    
class AdminUserViewSet(viewsets.ViewSet,
                        generics.ListAPIView,
                        generics.RetrieveAPIView):

    permission_classes = (IsAdminUser, )
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ['username', 'first_name', 'email', 'phone', 'address']
    ordering_fields = ['username', 'first_name', 'email', 'phone', 
                       'address', 'visits__time', 'visits'] #most_visits

    def get_serializer_class(self):
        if (self.action == 'retrieve' 
            and self.request.user.is_staff):
            return UserDetailSerializer
        if self.action == 'create':
            return UserRegistrationSerializer
        return UserSerializer
    
    def get_queryset(self):
        users = MyUser.is_admin.all()
        ordering_choices = self.request.query_params.get('ordering')
        if ordering_choices and 'most_visits' in ordering_choices.split(','):
            if '-most_visits' in ordering_choices.split(','):
                users= users.annotate(total_visits=Count('visits')).order_by('-total_visits')
                return users
            return users.annotate(total_visits=Count('visits')).order_by('total_visits')
        return users
    
class VisitViewSet(viewsets.ViewSet,
                   generics.ListAPIView):
    serializer_class = VisitSerializer
    queryset = Visit.objects.all()
    filter_backends = (OrderingFilter, )
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    serializer = UserDetailSerializer(request.user)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def verifyUser(request):
    return Response({
        'status': "ok"
    })
    
    
@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def accept_ordinary_user(request, id):
    user = get_object_or_404(MyUser, id=id, is_accepted=False)
    user.is_accepted = True
    user.save()
    # email = user.email
    # email_content = render_to_string('register_accepted_email.html')
    # plain_text = strip_tags(email_content)
    # send_mail('YOUR ACCOUNT IS NOW VALID',
    #             plain_text,
    #             EMAIL_HOST_USER,
    #             [email],
    #             html_message=email_content
    #           )

    return Response({'status': 'ok'})

@api_view(['POST'])
def get_user_from_refresh(request):
    refresh = request.data.get('refresh', None)
    if refresh:
        try:
            payload = jwt.decode(refresh, settings.SECRET_KEY, 'HS256')
            uid = payload['user_id']
            user = get_object_or_404(MyUser, id=uid)
            return Response(UserSerializer(user).data)
        except KeyError as a:
            return Response({'detail': 'Incorrect token'}, status=status.HTTP_400_BAD_REQUEST)
        except (jwt.DecodeError, jwt.ExpiredSignatureError) as e:
            return Response({'detail': 'Token may be expired or incorrect'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'detail': 'refresh token is required in body'}, status=status.HTTP_400_BAD_REQUEST)
