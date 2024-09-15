from django.contrib import admin
from members.models import Adresse, Client

class ClientAdmin(admin.ModelAdmin):
    list_display = ("nom", "prenom", "status", "date_inscription")
    list_editable = ("status", )

class AdresseAdmin(admin.ModelAdmin):
    list_display = ("app_unite","rue", "ville", "province", "code_postal")

admin.site.register(Client, ClientAdmin)
admin.site.register(Adresse, AdresseAdmin)

