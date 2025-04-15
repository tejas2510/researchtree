from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import ResearchProject, ProjectUpdate
from .forms import ResearchProjectForm, ProjectUpdateForm, ProgressUpdateForm
from users.models import CustomUser

@login_required
def project_list(request):
    # Different behavior based on user type
    if request.user.user_type == 'professor':
        # Professors see their own projects and other professors' projects in tabs
        own_projects = ResearchProject.objects.filter(owner=request.user)
        other_projects = ResearchProject.objects.exclude(owner=request.user)
        
        return render(request, 'projects/project_list.html', {
            'own_projects': own_projects,
            'other_projects': other_projects,
            'is_professor': True,
            'show_tabs': True  # Flag to show tabs in the template
        })
    else:
        # Students see all available projects
        projects = ResearchProject.objects.all()
        return render(request, 'projects/project_list.html', {
            'projects': projects,
            'is_professor': False,
            'show_tabs': False
        })

@login_required
def project_detail(request, project_id):
    project = get_object_or_404(ResearchProject, id=project_id)
    updates = project.updates.all()
    project_students = project.students.all()
    
    # Split skills into a list
    skills = [skill.strip() for skill in project.skills_required.split(',')] if project.skills_required else []
    
    # Check if current user is a student in this project
    is_member = request.user in project.students.all()
    
    # Check if current user is the owner
    is_owner = project.owner == request.user
    
    # Form for adding updates
    update_form = None
    progress_form = None
    
    if is_owner or is_member:
        update_form = ProjectUpdateForm()
        
    if is_owner:
        progress_form = ProgressUpdateForm(instance=project)
    
    # Handle update form submission
    if request.method == 'POST' and 'submit_update' in request.POST:
        update_form = ProjectUpdateForm(request.POST)
        if update_form.is_valid():
            update = update_form.save(commit=False)
            update.project = project
            update.created_by = request.user
            update.save()
            messages.success(request, 'Update added successfully!')
            return redirect('project_detail', project_id=project.id)
            
    # Handle progress update
    if request.method == 'POST' and 'update_progress' in request.POST:
        if not is_owner:
            return HttpResponseForbidden("You don't have permission to update project progress.")
            
        progress_form = ProgressUpdateForm(request.POST, instance=project)
        if progress_form.is_valid():
            progress_form.save()
            messages.success(request, 'Project progress updated!')
            return redirect('project_detail', project_id=project.id)
    
    return render(request, 'projects/project_detail.html', {
        'project': project,
        'updates': updates,
        'is_member': is_member,
        'is_owner': is_owner,
        'update_form': update_form,
        'progress_form': progress_form,
        'project_students': project_students,
        'skills': skills,
    })

@login_required
def apply_to_project(request, project_id):
    project = get_object_or_404(ResearchProject, id=project_id)
    
    # Only students can apply
    if request.user.user_type != 'student':
        messages.error(request, "Only students can apply to research projects.")
        return redirect('project_detail', project_id=project.id)
    
    # Check if the project is full
    if project.students.count() >= project.max_students:
        messages.error(request, "This project has reached its maximum student capacity.")
        return redirect('project_detail', project_id=project.id)
    
    # Add the student to the project
    project.students.add(request.user)
    messages.success(request, f"You have successfully applied to '{project.title}'.")
    
    # Redirect back to the project
    return redirect('project_detail', project_id=project.id)

@login_required
def project_create(request):
    # Only professors can create projects
    if request.user.user_type != 'professor':
        messages.error(request, "Only professors can create research projects.")
        return redirect('project_list')
        
    if request.method == 'POST':
        form = ResearchProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            messages.success(request, 'Research project created successfully!')
            return redirect('project_detail', project_id=project.id)
    else:
        form = ResearchProjectForm()
        
    return render(request, 'projects/project_form.html', {'form': form, 'is_new': True})

@login_required
def project_edit(request, project_id):
    project = get_object_or_404(ResearchProject, id=project_id)
    
    # Only the owner can edit the project
    if project.owner != request.user:
        return HttpResponseForbidden("You don't have permission to edit this project.")
        
    if request.method == 'POST':
        form = ResearchProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Research project updated successfully!')
            return redirect('project_detail', project_id=project.id)
    else:
        form = ResearchProjectForm(instance=project)
        
    return render(request, 'projects/project_form.html', {'form': form, 'is_new': False})

@login_required
def project_delete(request, project_id):
    project = get_object_or_404(ResearchProject, id=project_id)
    
    # Only the owner can delete the project
    if project.owner != request.user:
        return HttpResponseForbidden("You don't have permission to delete this project.")
    
    if request.method == 'POST':
        project_title = project.title
        project.delete()
        messages.success(request, f'Project "{project_title}" deleted successfully.')
        return redirect('project_list')
    
    return redirect('project_detail', project_id=project.id)

@login_required
def manage_students(request, project_id):
    project = get_object_or_404(ResearchProject, id=project_id)
    
    # Only the owner can manage students
    if project.owner != request.user:
        return HttpResponseForbidden("You don't have permission to manage students for this project.")
    
    if request.method == 'POST':
        # Add or remove student
        action = request.POST.get('action')
        student_id = request.POST.get('student_id')
        
        if action and student_id:
            try:
                student = CustomUser.objects.get(id=student_id)
                
                if action == 'add' and student.user_type == 'student':
                    # Check if project is full before adding
                    if project.students.count() >= project.max_students:
                        messages.error(request, "This project has reached its maximum student capacity.")
                    else:
                        project.students.add(student)
                        messages.success(request, f"{student.get_full_name()} added to the project.")
                    
                elif action == 'remove':
                    project.students.remove(student)
                    messages.success(request, f"{student.get_full_name()} removed from the project.")
                    
            except CustomUser.DoesNotExist:
                messages.error(request, "Student not found.")
    
    # Get potential students (those who aren't already in the project)
    current_students = project.students.all()
    potential_students = CustomUser.objects.filter(user_type='student').exclude(id__in=current_students.values_list('id', flat=True))
    
    return render(request, 'projects/manage_students.html', {
        'project': project,
        'current_students': current_students,
        'potential_students': potential_students
    })