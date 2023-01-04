from django.shortcuts import render
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from accounts.serializers import VisitWithUserSerializer
from accounts.models import Visit
import json
# Create your views here.

MyUser = get_user_model()

# get face data
def encoding(request):
    pass

# new face recognised
@api_view(['POST'])
def new_visit(request):

    uid = request.data['id']
    recent_visit = Visit.objects.filter(user__id=uid).order_by('-id').first()

    if not recent_visit:
        user = MyUser.is_ordinary.get(id=uid)
        if not user:
            return Response(status=HTTP_400_BAD_REQUEST)
        recent_visit = Visit.objects.create(user=user)

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'admin', {
            'type': 'notification_visit',
            'message': json.dumps(
                VisitWithUserSerializer(recent_visit).data
            )
        }
    )

    return Response(status=HTTP_200_OK)

