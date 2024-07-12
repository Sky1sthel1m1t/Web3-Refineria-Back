from django.urls import path, include
from rest_framework import routers

from api.viewsets import LoginViewSet, CamionViewSet, RutaViewSet

router = routers.DefaultRouter()
router.register(r'camiones', CamionViewSet)
router.register(r'rutas', RutaViewSet)
router.register('', LoginViewSet, basename='login')

urlpatterns = [
    path('', include(router.urls)),
]