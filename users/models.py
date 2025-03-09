from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('professor', 'Professor'),
        ('admin', 'Administrator'),
    )
    
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='student')
    department = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    profile_completed = models.BooleanField(default=False)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    
    # Additional fields for students
    skills = models.TextField(blank=True, help_text="Comma-separated list of skills")
    year_of_study = models.PositiveSmallIntegerField(null=True, blank=True)
    
    # Additional fields for professors
    title = models.CharField(max_length=50, blank=True)
    office_location = models.CharField(max_length=100, blank=True)
    office_hours = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return self.email