from django.shortcuts import render, get_object_or_404
from django.core import serializers
from django.template.context_processors import request

from .utils import compte_json
from accounts.models import Compte, Carte
from members.decorateurs import client_login_required, client_content


@client_content
@client_login_required
def dashboard(request):
    context = {}
    if getattr(request, 'is_visiteur', False):
        print("j'y suis enfin")
        # Contenu spécial pour les visiteurs
        context.update({
            'client': request.session.get('client_name'),
            'special_content': True,
            'status': "visiteur",
        })
    elif getattr(request, 'is_bloqued', False):
        print("le client est bloque ou inactif")
        context.update({
            'client_name': request.session.get('client_name'),
            'special_content': True,
            'status': "bloque",
        })
    else:
        print(request.session.get('is_invite'))
        carte_credit = None
        somme_total_compte = 0
        somme_total_carte = 0
        # Je recup l'id du client connecter depuis la session
        client_id = request.session["client_id"]
        # Maintenant je vais recup son compte courant sachant qu'il en a que un
        try:
            compte_courant = Compte.objects.get(client_id=client_id, type_compte="courant")
            somme_total_compte += float(compte_courant.solde)
        except Compte.DoesNotExist:
            compte_courant = None

        # Ensuite je recupere le ou les comptes epargne du client
        try:
            comptes_epargne = Compte.objects.filter(client_id=client_id, type_compte="epargne")
            for compte in comptes_epargne:
                somme_total_compte += float(compte.solde)
        except Compte.DoesNotExist:
            comptes_epargne = None

        # Enfin je recup le compte credit
        try:
            compte_credit = Compte.objects.get(client_id=client_id, type_compte="credit")
            try:
                carte_credit = Carte.objects.get(compte_id=compte_credit.id)
            except Carte.DoesNotExist:
                carte_credit = None
        except Compte.DoesNotExist:
            compte_credit = None

        context.update({
            'special_content': False,
            'status': False,
            'compte_courant': compte_courant,
            'comptes_epargne': comptes_epargne,
            'compte_credit': compte_credit,
            'carte_credit': carte_credit,
        })
        request.session['compte_courant'] = compte_json(compte_courant)

        request.session["client_solde_total"] = "{:,.2f}".format(somme_total_compte).replace(",", " ")
    return render(request, 'accounts/pages/dashboard.html', context)


def compte(request, numero_compte):
    compte = get_object_or_404(Compte, numero_compte=numero_compte)
    print(compte)
    return render(request, 'accounts/pages/compte.html', {'compte': compte})