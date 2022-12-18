from. import views
from django.urls import include, path
from rest_framework import routers
from .views import (
    AdminUserViewSet,
    OrdinaryUserViewSet,
    VisitViewSet
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from accounts.auth import MyTokenObtainPairView, MyTokenRefreshView

router = routers.DefaultRouter()
router.register('admin', AdminUserViewSet, 'admins')
router.register('ordinary', OrdinaryUserViewSet, 'ordinary-users')
router.register('visit', VisitViewSet, 'visits')

urlpatterns = [
    path('detect/', views.detect_face_by_img),
    path('', include(router.urls)),
    path('verify/', views.verifyUser),
    path('profile/', views.profile),
    path('auth/token/', MyTokenObtainPairView.as_view()),
    path('auth/token/refresh/', MyTokenRefreshView.as_view()),
    path('ordinary/<int:id>/accept/', views.accept_ordinary_user),
    path('auth/token/detail/', views.get_user_from_refresh)
]