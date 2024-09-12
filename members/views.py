from django.views.generic import TemplateView


class LoginView(TemplateView):
    template_name = 'members/auth/login.html'




class ResetPasswordView(TemplateView):
    pass



class RegisterView(TemplateView):
    pass