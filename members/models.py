from datetime import timedelta, date

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
# from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


# class ClientManager(BaseUserManager):
#     def create_client(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError('Vous etes oblige de rentrer un adresse email')
#
#         user = self.model(email=self.normalize_email(email), **extra_fields)
#         user.set_password(password)
#         user.save()
#         return user

    # def create_superuser(self, email, password=None):
    #     user = self.create_user(email=email, password=password)
    #     user.is_staff = True
    #     user.is_admin = True
    #     user.is_superuser = True
    #     user.save()
    #     return user





class Adresse(models.Model):
    rue = models.CharField(max_length=255)
    ville = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    code_postal = models.CharField(max_length=10)
    app_unite = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        # if self.app_unite is not None:
        #     return f"{self.app_unite} {self.rue} {self.ville} {self.province} {self.code_postal}"
        return f"{self.app_unite} {self.rue} {self.ville} {self.province} {self.code_postal}"


class Client(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),  # l'utilisateur est membre et son compte est actif
        ("inactive", "Inactive"),  # L'utilisateur a son compte desactive temporairement
        ("visiteur", "Visiteur"),
        # Le compte de l'utilisateur n'est pas encore confirme, c'est un simple visiteur a ce stade
        ("bloque", "Bloque"),  # Le compte de l'utilisateur est bloque, il ne peut faire aucune transaction
    ]

    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True, blank=False, max_length=254)
    password = models.CharField(max_length=128)
    telephone = models.CharField(unique=True)
    date_inscription = models.DateField(auto_now_add=True)
    date_naissance = models.DateField(null=False, blank=False, default=date(2004, 1, 1))
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="visiteur")
    adresse = models.ForeignKey(Adresse, on_delete=models.SET_NULL, null=True, blank=True)
    genre = models.CharField(max_length=100, choices=[("M", "Masculin"), ("F", "Feminin"), ("X", "Sac Walmart")],
                             default="Masculin")
    is_first = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)  # Un User par defaut est active

    # objects = ClientManager()

    USERNAME_FIELD = "email"  # Le champ qu'on utilise pour ce connecter
    # REQUIRED_FIELDS = ["nom", "prenom", "date_naissance", "telephone"]  # Les champs obligatoire

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, perm, obj=None):
        return True

    class Meta:
        ordering = ['nom']

    # Le schema d'affichage de mes donnees
    def __str__(self):
        return f'{self.nom}, {self.prenom} ({self.status}) {str(self.date_inscription)}'

    # HAchage du mdp avant la sauvegarde
    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith("pbkdf2_sha256$"):
            self.password = make_password(self.password)

        super().save(*args, **kwargs)

    # Verifier si l'utilisateur qui s'inscrit est majeur. Autrepasse si un admin qui ouvre le compte
    def clean(self):
        super().clean()
        if self.date_naissance:
            age_limit = timezone.now().date() - timedelta(days=18 * 365)
            if self.date_naissance > age_limit:
                raise ValidationError("Vous devez avoir au moins 18 ans pour ouvrir un compte.")
