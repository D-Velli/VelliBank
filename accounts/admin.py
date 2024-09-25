import random
from datetime import timedelta

from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.utils import timezone

from members.models import Client
from .models import Compte, Carte

class CompteForm(forms.ModelForm):
    class Meta:
        model = Compte
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrer les clients, ici on affiche tous les clients
        self.fields['client'] = forms.ModelChoiceField(
            queryset=Client.objects.all(),
            label="Client",
            required=True,
            widget=forms.Select
        )
        # Personnaliser l'affichage du client dans la liste déroulante
        self.fields["client"].label_from_instance = lambda obj: f"{obj.prenom} {obj.nom} - {obj.email}"


class CompteAdmin(admin.ModelAdmin):
    form = CompteForm
    list_display = ("numero_compte", "type_compte", "status_compte", "date_creation")
    list_editable = ("status_compte",)
    readonly_fields = ("numero_compte",)

    def save_model(self, request, obj, form, change):
        # Générer un numéro de compte si celui-ci est vide
        if not obj.numero_compte:
            if obj.type_compte == 'epargne':
                # Récupérer le nombre de comptes épargne existants pour le client et ajouter 1 pour l'indice
                indice = Compte.objects.filter(client=obj.client, type_compte='epargne').count() + 1
                obj.numero_compte = f"{''.join([str(random.randint(0, 9)) for _ in range(6)])}-CE{indice}"
            elif obj.type_compte == 'credit':
                obj.numero_compte = f"{''.join([str(random.randint(0, 9)) for _ in range(6)])}-CC"
        super().save_model(request, obj, form, change)

class CarteForm(forms.ModelForm):
    class Meta:
        model = Carte
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrer les comptes pour n'afficher que ceux de type "crédit"
        self.fields['compte'] = forms.ModelChoiceField(
            queryset=Compte.objects.filter(type_compte='credit'),
            label="Compte",
            required=True,
            widget=forms.Select
        )
        # Personnaliser les options pour afficher le nom et prénom du client associé
        self.fields['compte'].label_from_instance = lambda obj: f"{obj.client.prenom} {obj.client.nom} - {obj.numero_compte}"


class CarteAdmin(admin.ModelAdmin):
    form = CarteForm
    list_display = ("numero_carte", "type_carte", "status", "date_emission")
    list_editable = ("status", )
    readonly_fields = ('numero_carte', 'cvv', 'date_emission', 'date_expiration')


    def save_model(self, request, obj, form, change):

        # Appeler la méthode clean() pour exécuter la validation du modèle
        try:
            obj.clean()
        except ValidationError as e:
            # Si une validation échoue, Django lèvera une erreur dans l'admin
            self.message_user(request, f"Erreur : {e}", level='error')
            return
        # Générer automatiquement un numéro de carte (16 chiffres)
        if not obj.numero_carte:
            if not obj.numero_carte:
                obj.numero_carte = ' '.join(
                    ''.join([str(random.randint(0, 9)) for _ in range(16)])[i:i + 4] for i in range(0, 16, 4))

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
