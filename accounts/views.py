from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import (
    viewsets,
    generics,
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
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
    
    parser_classes = (MultiPartParser, FormParser)
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