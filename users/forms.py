from django import forms
from .models import CustomUser

class ProfileSetupForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'department', 'bio', 'profile_image', 
                  'title', 'office_location', 'office_hours',  # Add these fields
                  'skills', 'year_of_study']  # Add the student fields too
        
    def __init__(self, *args, **kwargs):
        user_type = kwargs.pop('user_type', None)
        super().__init__(*args, **kwargs)
        
        # Add fields based on user type
        if user_type == 'student':
            self.fields['skills'] = forms.CharField(
                widget=forms.Textarea,
                required=False,
                help_text="Comma-separated list of skills"
            )
            self.fields['year_of_study'] = forms.IntegerField(required=False)
            
        elif user_type == 'professor':
            self.fields['title'] = forms.CharField(max_length=50, required=False)
            self.fields['office_location'] = forms.CharField(max_length=100, required=False)
            self.fields['office_hours'] = forms.CharField(max_length=200, required=False)