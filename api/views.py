# api/views.py
from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>Welcome to the Django API</h1>")

