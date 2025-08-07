from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


from .views import (
    AnggotaViewSet,
    TabunganViewSet,
    PinjamanViewSet,
    ProfileViewSet   # tambahkan viewset profile
)

router = DefaultRouter()
router.register(r'anggota', AnggotaViewSet)
router.register(r'tabungan', TabunganViewSet)
router.register(r'pinjaman', PinjamanViewSet)
router.register(r'profile', ProfileViewSet, basename='profile')  # tambahkan ini

urlpatterns = [
    path('', include(router.urls)),

    # login pakai JWT
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
