from datetime import timedelta
import random

from django.core.exceptions import ValidationError
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

    def save(self, *args, **kwargs):
        super(Compte, self).save(*args, **kwargs)
        # Si le compte est de type "crédit", synchroniser le solde avec le solde disponible de la carte
        if self.type_compte == 'credit':
            # Récupérer la carte associée (si elle existe)
            carte = self.carte_set.first()  # Récupérer la première carte liée
            if carte:
                carte.solde_disponible = self.solde
                carte.save()




    def clean(self):
        # Vérifier que le client n'a pas déjà un compte de type "courant"
        if self.type_compte == 'courant' and Compte.objects.filter(client=self.client, type_compte='courant').exists():
            raise ValidationError('Ce client a déjà un compte de type courant.')

    def __str__(self):
        return f"{self.numero_compte} {self.type_compte} {self.status_compte} {self.date_creation}"




class Carte(models.Model):
    TYPE_CARTE = [
        ("Visa", "Visa"),
        ("MasterCard", "MasterCard"),
    ]

    STATUS_CARTE = [
        ("active", "Active"),
        ("bloque", "Bloqué"),
        ("expired", "Expiré"),
    ]
    compte = models.ForeignKey(Compte, on_delete=models.CASCADE)
    type_carte = models.CharField(max_length=50, choices=TYPE_CARTE)
    numero_carte = models.CharField(max_length=20, unique=True)
    cvv = models.IntegerField()
    date_emission = models.DateTimeField(auto_now_add=True)
    limite_credit = models.DecimalField(max_digits=10, decimal_places=2, default=500.00)
    status = models.CharField(max_length=50, choices=STATUS_CARTE, default="active")
    solde_disponible = models.DecimalField(max_digits=10, decimal_places=2)
    code_pin = models.IntegerField()
    date_expiration = models.DateField()


    def save(self, *args, **kwargs):
        # Synchroniser le solde du compte crédit avec le solde disponible de la carte
        if self.compte.type_compte == 'credit':
            self.compte.solde = self.solde_disponible
            self.compte.save()  # Sauvegarder le compte mis à jour

        super(Carte, self).save(*args, **kwargs)

    def clean(self):
        # Vérifier que le compte associé est de type "crédit"
        if self.compte.type_compte != 'credit':
            raise ValidationError("Les cartes ne peuvent être associées qu'à des comptes de type 'crédit'.")

    def __str__(self):
        return f"{self.numero_carte} {self.type_carte} {self.status} {self.date_emission}"
