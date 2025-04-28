from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Admin(models.Model):
    role_choices = [
        ('bendahara', 'Bendahara'),
        ('sekretaris', 'Sekretaris'),
        ('ketua', 'Ketua'),
    ]

    username = models.CharField(max_length=50, unique=True)
    password_hash = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=role_choices, default='ketua')

    def __str__(self):
        return self.username

    def set_password(self, raw_password):
        self.password_hash = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password_hash)