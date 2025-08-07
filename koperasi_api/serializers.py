from rest_framework import serializers
from anggota.models import Anggota

class AnggotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anggota
        fields = '__all__'

from tabungan.models import Tabungan

class TabunganSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tabungan
        fields = '__all__'

from pinjaman.models import Pinjaman

class PinjamanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pinjaman
        fields = '__all__'

from anggota.models import Anggota

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anggota
        fields = ['id', 'user', 'alamat', 'no_hp']
        read_only_fields = ['user']


