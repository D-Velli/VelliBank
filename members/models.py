from django.db import models
from django.contrib.auth.hashers import make_password


class Adresse(models.Model):
    rue = models.CharField(max_length=255)
    ville = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    code_postal = models.CharField(max_length=10)
    app_unite = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.rue} {self.ville} {self.province} {self.code_postal}"


class Client(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"), # l'utilisateur est membre et son compte est actif
        ("inactive", "Inactive"), # L'utilisateur a son compte desactive temporairement
        ("visiteur", "Visiteur"), # Le compte de l'utilisateur n'est pas encore confirme, c'est un simple visiteur a ce stade
        ("bloque", "Bloque"), # Le compte de l'utilisateur est bloque, il ne peut faire aucune transaction
    ]

    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    numero = models.CharField(unique=True)
    date_inscription = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="visiteur")
    adresse = models.OneToOneField(Adresse, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['nom']


    def __str__(self):
        return f'{self.nom}, {self.prenom} ({self.status}) {str(self.date_inscription)}'


    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith("pbkdf2_sha256$"):
            self.password = make_password(self.password)

        super().save(*args, **kwargs)




