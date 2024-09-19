from django.shortcuts import redirect

def client_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if 'client_id' not in request.session:
            # Rediriger vers la page de connexion si l'utilisateur n'est pas connecté
            return redirect('members:login')
        # Sinon, exécuter la vue
        return view_func(request, *args, **kwargs)
    return wrapper
