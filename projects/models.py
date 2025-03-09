from django.db import models
from django.conf import settings

class ResearchProject(models.Model):
    STATUS_CHOICES = (
        ('planning', 'Planning'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    niche = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planning')
    progress = models.PositiveSmallIntegerField(default=0, help_text="Progress percentage (0-100)")
    
    # Requirements
    department_requirement = models.CharField(max_length=100, blank=True)
    skills_required = models.TextField(blank=True, help_text="Comma-separated list of required skills")
    max_students = models.PositiveSmallIntegerField(default=5)
    
    # Dates
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    
    # Relationships
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_projects'
    )
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name='joined_projects',
        blank=True
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-updated_at']


class ProjectUpdate(models.Model):
    project = models.ForeignKey(ResearchProject, on_delete=models.CASCADE, related_name='updates')
    content = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Update for {self.project.title} on {self.created_at.strftime('%Y-%m-%d')}"
    
    class Meta:
        ordering = ['-created_at']
