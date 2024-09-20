import random
from datetime import timedelta

from django.contrib import admin
from django.utils import timezone

from .models import Compte, Carte

class CompteAdmin(admin.ModelAdmin):
    list_display = ("numero_compte", "type_compte", "status_compte", "date_creation")
    list_editable = ("status_compte",)

class CarteAdmin(admin.ModelAdmin):
    list_display = ("numero_carte", "type_carte", "status", "date_emission")
    list_editable = ("status", )
    readonly_fields = ('numero_carte', 'cvv', 'date_emission', 'date_expiration')

    def save_model(self, request, obj, form, change):
        # Générer automatiquement un numéro de carte (16 chiffres)
        if not obj.numero_carte:
            obj.numero_carte = ''.join([str(random.randint(0, 9)) for _ in range(16)])

        # Générer automatiquement un CVV (3 chiffres)
        if not obj.cvv:
            obj.cvv = random.randint(100, 999)

        # Définir la date d'expiration comme étant 2 ans après la date d'émission
        if not obj.date_expiration:
            obj.date_expiration = timezone.now() + timedelta(days=2 * 365)

        # Appeler la méthode `save` de la classe parente pour enregistrer l'objet
        super().save_model(request, obj, form, change)


admin.site.register(Compte, CompteAdmin)
admin.site.register(Carte, CarteAdmin)
