from django.db import models

class Admin(models.Model):
    role_choices = [('bendahara', 'Bendahara'), ('sekretaris', 'Sekretaris'), ('anggota', 'Anggota')]

    username = models.CharField(max_length=50, unique=True)
    password_hash = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=role_choices, default='anggota')

    def __str__(self):
        return self.username
