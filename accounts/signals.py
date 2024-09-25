from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Compte, Client
import random

@receiver(post_save, sender=Client)
def create_compte(sender, instance, created, **kwargs):
    if created:
        # Générer un numéro de compte unique
        numero_compte = ''.join([str(random.randint(0, 9)) for _ in range(6)]) + "-COC"

        # Vérifier que le numéro est unique
        while Compte.objects.filter(numero_compte=numero_compte).exists():
            numero_compte = ''.join([str(random.randint(0, 9)) for _ in range(6)]) + "-COC"

        # Créer un compte pour le client
        Compte.objects.create(
            client=instance,
            numero_compte=numero_compte,
            type_compte='courant',  # Par défaut, un compte courant est créé
            solde=0.00,  # Solde initial
        )

@receiver(post_save, sender=Client)
def save_compte(sender, instance, **kwargs):
    instance.compte_set.all().update(client=instance)
