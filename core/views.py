from django.shortcuts import render
from django.core.management import call_command
from django.http import HttpResponse
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')
    
def create_superuser(request):
    try:
        # Replace with your superuser credentials
        call_command('createsuperuser', '--username', 'admin', '--email', 'admin@example.com', '--noinput')
        return HttpResponse("Superuser created successfully!")
    except Exception as e:
        return HttpResponse(f"Error: {e}")
