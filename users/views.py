from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProfileSetupForm
from .models import CustomUser

@login_required
def profile_setup(request):
    # Redirect if profile is already completed
    if request.user.profile_completed:
        return redirect('profile-setup')
        
    if request.method == 'POST':
        form = ProfileSetupForm(request.POST, request.FILES, instance=request.user, user_type=request.user.user_type)
        if form.is_valid():
            user = form.save(commit=False)
            user.profile_completed = True
            user.save()
            messages.success(request, 'Profile set up successfully!')
            return redirect('dashboard')
    else:
        form = ProfileSetupForm(instance=request.user, user_type=request.user.user_type)
    
    return render(request, 'users/profile_setup.html', {'form': form,'user': request.user})

@login_required
def profile_view(request, user_id=None):
    if user_id:
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            messages.error(request, 'User not found.')
            return redirect('dashboard')
    else:
        user = request.user
    
    # Process skills list for student profiles
    skills = []
    if user.user_type == 'student' and user.skills:
        skills = [skill.strip() for skill in user.skills.split(',')]
        
    return render(request, 'users/profile_view.html', {
        'profile_user': user,
        'skills': skills
    })

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileSetupForm(request.POST, request.FILES, instance=request.user, user_type=request.user.user_type)
        if form.is_valid():
            user = form.save(commit=False)
            
            # For professors, explicitly save these fields
            if user.user_type == 'professor':
                if 'title' in form.cleaned_data:
                    user.title = form.cleaned_data['title']
                if 'office_location' in form.cleaned_data:
                    user.office_location = form.cleaned_data['office_location']
                if 'office_hours' in form.cleaned_data:
                    user.office_hours = form.cleaned_data['office_hours']
            
            # Save the user object
            user.save()
            
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile_view')
    else:
        form = ProfileSetupForm(instance=request.user, user_type=request.user.user_type)
    
    return render(request, 'users/profile_edit.html', {'form': form})