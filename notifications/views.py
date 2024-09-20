from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "notifications/register_confirmation.html")