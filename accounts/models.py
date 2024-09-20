from datetime import timedelta
import random

from django.db import models
from django.utils import timezone

from members.models import Client

class Compte(models.Model):
    TYPE_COMPTE = [
        ("courant", "Courant"),
        ("epargne", "Epargne"),
        ("credit", "Credit"),
    ]

    STATUS_COMPTE = [
        ("actif", "Actif"),
        ("suspendu", "Suspendu"),
        ("bloque", "Bloque"),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    numero_compte = models.CharField(max_length=10, unique=True)
    type_compte = models.CharField(max_length=50, choices=TYPE_COMPTE)
    solde = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status_compte = models.CharField(max_length=50, choices=STATUS_COMPTE, default="actif")
    date_creation = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.numero_compte} {self.type_compte} {self.status_compte} {self.date_creation}"




class Carte(models.Model):
    TYPE_CARTE = [
        ("visa", "Visa"),
        ("mastercard", "Mastercard"),
    ]

    STATUS_CARTE = [
        ("active", "Active"),
        ("bloque", "Bloqué"),
        ("expired", "Expiré"),
    ]
    compte = models.ForeignKey(Compte, on_delete=models.CASCADE)
    type_carte = models.CharField(max_length=50, choices=TYPE_CARTE)
    numero_carte = models.CharField(max_length=16, unique=True)
    cvv = models.IntegerField()
    date_emission = models.DateTimeField(auto_now_add=True)
    limite_credit = models.DecimalField(max_digits=10, decimal_places=2, default=500.00)
    status = models.CharField(max_length=50, choices=STATUS_CARTE, default="active")
    solde_disponible = models.DecimalField(max_digits=10, decimal_places=2)
    code_pin = models.IntegerField()
    date_expiration = models.DateField()


    def __str__(self):
        return f"{self.numero_carte} {self.type_carte} {self.status} {self.date_emission}"
