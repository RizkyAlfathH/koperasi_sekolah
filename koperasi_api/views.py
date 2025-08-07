from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from anggota.models import Anggota
from tabungan.models import Tabungan
from pinjaman.models import Pinjaman


from .serializers import (
    AnggotaSerializer,
    TabunganSerializer,
    PinjamanSerializer,
    ProfileSerializer   # tambahkan serializer profile
)

class AnggotaViewSet(viewsets.ModelViewSet):
    queryset = Anggota.objects.all()
    serializer_class = AnggotaSerializer

class TabunganViewSet(viewsets.ModelViewSet):
    queryset = Tabungan.objects.all()
    serializer_class = TabunganSerializer

class PinjamanViewSet(viewsets.ModelViewSet):
    queryset = Pinjaman.objects.all()
    serializer_class = PinjamanSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    # hanya data milik user login
    def get_queryset(self):
        return Anggota.objects.filter(user=self.request.user)

    # kalau update, pastikan user sama
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
