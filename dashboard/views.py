from django.shortcuts import render, redirect  # Add 'redirect'
from django.contrib.auth.decorators import login_required
from projects.models import ResearchProject

@login_required
def dashboard(request):
    # Check if profile is completed, if not redirect to profile setup
    if not request.user.profile_completed:
        return redirect('profile_setup')
        
    # Different dashboard for different user types
    if request.user.user_type == 'professor':
        # For professors
        owned_projects = ResearchProject.objects.filter(owner=request.user)
        
        # Count students in each project
        for project in owned_projects:
            project.student_count = project.students.count()
            
        return render(request, 'dashboard/professor_dashboard.html', {
            'owned_projects': owned_projects,
        })
        
    elif request.user.user_type == 'student':
        # For students
        joined_projects = request.user.joined_projects.all()
        available_projects = ResearchProject.objects.exclude(
            id__in=joined_projects.values_list('id', flat=True)
        )
        
        return render(request, 'dashboard/student_dashboard.html', {
            'joined_projects': joined_projects,
            'available_projects': available_projects[:5]  # Show only 5 recent ones
        })
        
    else:
        # For administrators
        all_projects = ResearchProject.objects.all()
        projects_by_department = {}
        
        for project in all_projects:
            dept = project.department_requirement or "General"
            if dept not in projects_by_department:
                projects_by_department[dept] = []
            projects_by_department[dept].append(project)
            
        return render(request, 'dashboard/admin_dashboard.html', {
            'all_projects': all_projects,
            'projects_by_department': projects_by_department,
        })