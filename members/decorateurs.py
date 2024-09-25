from django.shortcuts import redirect
from functools import wraps

def client_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if 'client_id' not in request.session:
            # Rediriger vers la page de connexion si l'utilisateur n'est pas connecté
            return redirect('members:login')
        # Sinon, exécuter la vue
        return view_func(request, *args, **kwargs)
    return wrapper


from functools import wraps
from django.shortcuts import redirect


def client_invite(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        client_status = request.session.get('client_status')
        print(client_status)
        if client_status == 'visiteur':
            # Si le client est invité, ajoute l'attribut à la requête
            request.is_invite = True
            print("Client invité détecté.")
        else:
            # Le client n'est pas invité
            request.is_invite = False
            print("Client non invité ou statut introuvable.")

        # Appel de la vue d'origine
        return view_func(request, *args, **kwargs)

    return _wrapped_view
