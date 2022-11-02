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

router = routers.DefaultRouter()
router.register('admin', AdminUserViewSet, 'admins')
router.register('ordinary', OrdinaryUserViewSet, 'ordinary-users')
router.register('visit', VisitViewSet, 'visits')

urlpatterns = [
    path('detect/', views.detect_face_by_img),
    path('', include(router.urls)),
    path('profile/', views.profile),
    path('auth/token/', TokenObtainPairView.as_view()),
    path('auth/token/refresh/', TokenRefreshView.as_view()),
]