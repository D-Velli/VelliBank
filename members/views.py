from django.views.generic import TemplateView


class LoginView(TemplateView):
    template_name = 'members/auth/login.html'



class ResetPasswordView(TemplateView):
    template_name = "members/reset-password.html"



class RegisterView(TemplateView):
    template_name = 'members/auth/register.html'