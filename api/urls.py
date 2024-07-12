from django.urls import path, include
from rest_framework import routers

from api.viewsets import LoginViewSet, CamionViewSet, RutaViewSet, ChoferViewSet

router = routers.DefaultRouter()
router.register(r'camiones', CamionViewSet)
router.register(r'rutas', RutaViewSet)
router.register(r'chofer', ChoferViewSet, basename='chofer')
router.register('', LoginViewSet, basename='login')

urlpatterns = [
    path('', include(router.urls)),
]