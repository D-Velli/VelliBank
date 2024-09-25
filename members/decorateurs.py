from django.shortcuts import redirect
from functools import wraps

from members.models import Client


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


def client_content(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # client_status = request.session.get('client_status')
        try :
            client = Client.objects.get(pk=request.session['client_id'])
        except Client.DoesNotExist :
            return redirect('members:login')
        client_status = client.status
        if client_status == 'visiteur':
            request.is_visiteur = True
            print("Client invité détecté.")
        elif client_status == 'bloque' or client_status == 'inactive':
            request.is_bloqued = True
            print("le client est bloque")
        else:
            request.is_invite = False
            request.is_bloqued = False
            print("Client membre.")

        # Appel de la vue d'origine
        return view_func(request, *args, **kwargs)

    return _wrapped_view
