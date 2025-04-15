from django.contrib.auth import get_user_model
def about(request):
    return render(request, 'about.html')
def home(request):
    return render(request, 'home.html')

def create_superuser(request):
    User = get_user_model()
    if not User.objects.filter(username='klayjensen').exists():
        User.objects.create_superuser(
            username='klayjensen',
            email='klay@example.com',
            password='Tejas2025$'
        )
        return HttpResponse("Superuser 'klayjensen' created with password 'Tejas2025$' ✅")
    return HttpResponse("Superuser 'klayjensen' already exists ❗")
