from django.shortcuts import render
from django.core.management import call_command
from django.http import HttpResponse
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')
def create_superuser(request):
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'YourSecurePassword123')
        return HttpResponse("Superuser created!")
    return HttpResponse("Superuser already exists.")


def reset_admin_password(request):
    User = get_user_model()
    try:
        user = User.objects.get(username='admin')
        user.set_password('YourSecurePassword123')  # change this to whatever you want
        user.save()
        return HttpResponse("Password reset successfully!")
    except User.DoesNotExist:
        return HttpResponse("Admin user does not exist.")
