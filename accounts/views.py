from django.shortcuts import render

from accounts.models import Compte, Carte
from members.decorateurs import client_login_required, client_invite


@client_invite
@client_login_required
def dashboard(request):
    context = {}
    if getattr(request, 'is_invite', False):
        print("j'y suis enfin")
        # Contenu spécial pour les invités
        context.update({
            'client': request.session.get('client_name'),
            'special_content': True,
        })
    else:

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
            'compte_courant': compte_courant,
            'comptes_epargne': comptes_epargne,
            'compte_credit': compte_credit,
            'carte_credit': carte_credit,
        })
        print(compte_courant.solde)
        print(compte_courant.type_compte)
        print(carte_credit.type_carte)
        # request.session["client_num_compte"] = client_compte_courant.numero_compte
        # request.session["client_solde"] = float(client_compte_courant.solde)
        request.session["client_solde_total"] = "{:,.2f}".format(somme_total_compte).replace(",", " ")
    return render(request, 'accounts/pages/dashboard.html', context)
