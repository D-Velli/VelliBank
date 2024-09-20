from django.contrib.messages import success
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password, check_password  # Pour hasher le mot de passe
from members.models import Client
from accounts.models import Compte, Carte
from notifications.tasks import send_registration_email, send_reset_password_email
from .decorateurs import client_login_required
from .utils import generate_password, format_phone_number, check_date_birthday, generate_random_password


def register(request):
    errors = {}
    form_data = {}

    if request.method == 'POST':
        email = request.POST.get('email')
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        date_birth = request.POST.get('date_birth')
        confirm_email = request.POST.get('confirm_email')
        telephone = request.POST.get('telephone')

        # Remplir form_data avec les valeurs soumises pour pré-remplir le formulaire en cas d'erreurs
        form_data = {
            'email': email,
            'nom': nom,
            'prenom': prenom,
            'date_birth': date_birth,
            'confirm_email': confirm_email,
            'telephone': telephone,
        }

        # Validation des champs
        if Client.objects.filter(email=email).exists():
            errors['email'] = "L'email est déjà utilisé par un autre client"
        if email != confirm_email:
            errors['email'] = 'Les adresses emails ne correspondent pas'
        if not format_phone_number(telephone):
            errors['telephone'] = "Numéro de téléphone invalide"
        if check_date_birthday(date_birth):
            errors['date'] = 'Vous devez avoir au moins 18 ans pour ouvrir un compte.'

        # Si des erreurs existent, renvoyer les données du formulaire avec les erreurs
        if errors:
            return render(request, "members/auth/register.html", {'errors': errors, 'form_data': form_data})

        # Si tout est valide, créer le client
        password = generate_password(nom=nom, prenom=prenom)
        client = Client.objects.create(
            nom=nom, prenom=prenom, date_naissance=date_birth,
            email=email, password=make_password(password), telephone=format_phone_number(telephone)
        )
        client.save()

        # Envoyer un email de confirmation
        send_registration_email.delay(client_email=email, client_mdp=password, client_name=f"{prenom} {nom}")

        # Rediriger vers la page de login avec un message de succès
        success = {
            'title': "Inscription réussie",
            'content': "Votre compte a été créé avec succès. Vous recevrez un email avec vos identifiants."
        }
        return redirect('members:login')

    # En cas de méthode GET, renvoyer le formulaire vide
    return render(request, 'members/auth/register.html')


def reset_password(request):
    errors = {}
    form_data = {}
    if request.method == 'POST':
        email = request.POST.get('email')  # Utilise .get() pour éviter KeyError si le champ est vide
        form_data['email'] = email
        print(email)
        if not email:
            errors['email'] = "Veuillez entrer une adresse email valide."
        else:
            try:
                # Récupérer le client avec l'email fourni
                client = Client.objects.get(email=email)
                # Générer un nouveau mot de passe
                password_generate = generate_random_password()
                # Mettre à jour le mot de passe en le hashant
                client.password = make_password(password_generate)
                client.is_first = True
                client.save()
                # Préparer les informations pour l'email
                nom = client.nom
                prenom = client.prenom
                # Envoyer l'email avec Celery
                send_reset_password_email.delay(
                    client_email=email,
                    client_mdp=password_generate,
                    client_name=f"{prenom} {nom}"
                )
                request.session["success"] = {
                    'title': "Réinitialisation réussie",
                    'content': "Un nouveau mot de passe vous a été envoyé par email."
                }
                # Ajouter un message de succès (par exemple via Django messages framework)
                return redirect("members:login")

            except ObjectDoesNotExist:
                # Si l'email n'existe pas dans la base de données
                errors['email'] = "Cette adresse n'est associée à aucun compte."

        # Si des erreurs sont présentes, on les renvoie à la vue
        if errors:
            return render(request, "members/reset-password.html", {'errors': errors, 'form_data': request.POST})

    # Affichage du formulaire vide si méthode GET
    return render(request, "members/reset-password.html")


def login(request):
    errors = {}
    form_data = {}
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        form_data['email'] = email
        if email and password:
            try:
                client = Client.objects.get(email=email)
                if check_password(password, client.password):
                    request.session["client_id"] = client.id
                    request.session["client_name"] = f"{client.prenom} {client.nom}"
                    client.is_first = False
                    client.save()
                    return redirect("members:dashboard")
                else:
                    errors['email'] = "Email ou Mot de passe invalide"
            except ObjectDoesNotExist:
                errors['email'] = "Email ou Mot de passe invalide"
        else:
            errors['email'] = "Vous devez remplir tout les champs"

        if errors:
            return render(request, "members/auth/login.html", {'errors': errors, 'form_data': form_data})

    return render(request, 'members/auth/login.html')


def logout(request):
    request.session.flush()  # Efface toute la session
    return redirect('members:login')

@client_login_required
def dashboard(request):
    # Je recup l'id du client connecter depuis la session
    client_id = request.session["client_id"]
    # Maintenant je vais recup son compte courant sachant qu'il en a que un
    try:
        compte_courant = Compte.objects.get(client_id=client_id, type_compte="courant")
    except Compte.DoesNotExist:
        compte_courant = None

    # Ensuite je recupere le ou les comptes epargne du client
    try:
        comptes_epargne = Compte.objects.filter(client_id=client_id, type_compte="epargne")
    except Compte.DoesNotExist:
        comptes_epargne = None

    context = {
        'compte_courant': compte_courant,
        'comptes_epargne': comptes_epargne,
    }

    print(compte_courant.solde)
    print(compte_courant.type_compte)
    # request.session["client_num_compte"] = client_compte_courant.numero_compte
    # request.session["client_solde"] = float(client_compte_courant.solde)
    # request.session["client_solde_total"] = float(client_compte.solde) + float(12)
    return render(request, 'members/pages/dashboard.html', context)








# class LoginView(TemplateView):
#     template_name = 'members/auth/login.html'
#     def post(self, request, *args, **kwargs):
#         email = request.POST['email']
#         password = request.POST['password']
#         print(email, password)
#         client = Client.objects.get(email=email)
#         if client.password == password:
#             return redirect(to="members:accueil")


# class ResetPasswordView(TemplateView):
#     template_name = "members/reset-password.html"
#
#
# class RegisterView(TemplateView):
#     template_name = 'members/auth/register.html'
#
#     def post(self, request, *args, **kwargs):
#         nom = request.POST.get('nom')
#         prenom = request.POST.get('prenom')
#         email = request.POST.get('email')
#         print(nom, prenom, email)
#         client = Client.objects.create_client(nom=nom, prenom=prenom, email=email, *args, **kwargs)
#         client.save()
#         return HttpResponse("Success")
