from django import forms
from .models import ResearchProject, ProjectUpdate

class ResearchProjectForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(
            attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Start Date'}
        ),
        required=False
    )
    end_date = forms.DateField(
        widget=forms.DateInput(
            attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'End Date'}
        ),
        required=False
    )

    class Meta:
        model = ResearchProject
        fields = [
            'title', 'description', 'niche', 'status', 'progress',
            'department_requirement', 'skills_required', 'max_students',
            'start_date', 'end_date'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Project Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Project Description'}),
            'niche': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Project Niche'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'progress': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Progress in %'}),
            'department_requirement': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Department Requirement'}),
            'skills_required': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Required Skills'}),
            'max_students': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Max Students'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),

        }

class ProjectUpdateForm(forms.ModelForm):
    class Meta:
        model = ProjectUpdate
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Update Content'}),
        }
        
class ProgressUpdateForm(forms.ModelForm):
    class Meta:
        model = ResearchProject
        fields = ['progress', 'status']
        widgets = {
            'progress': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Update Progress in %'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
