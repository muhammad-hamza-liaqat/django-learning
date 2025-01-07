from django.http import HttpResponse

def home(request):
    return HttpResponse("Development server, Home route")
