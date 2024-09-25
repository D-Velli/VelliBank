import json

from accounts.models import Compte


def compte_json(numero_compte):
    try:
        comptes = Compte.objects.filter(numero_compte=numero_compte)
    except Compte.DoesNotExist:
        comptes = []
    if isinstance(comptes, Compte):
        comptes = [comptes]
    comptes_list = [
        {
            'id_compte' : compte.id,
            'numero_compte': compte.numero_compte,
            'type_compte': compte.type_compte,
            'status': compte.status_compte,
            'date_creation': compte.date_creation.isoformat(),
            'solde': float(compte.solde)
        }
        for compte in comptes
    ]

    return json.loads(json.dumps(comptes_list))
