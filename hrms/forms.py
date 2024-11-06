from django import forms
from .models import JobPost

class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = ['job_title', 'job_description', 'job_requirements']

        widgets = {
            'job_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter job title',
                'maxlength': 100
            }),
            'job_description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter job description',
                'rows': 4,
            }),
            'job_requirements': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter job requirements',
                'rows': 3,
            }),
        }

        labels = {
            'job_title': 'Job Title',
            'job_description': 'Job Description',
            'job_requirements': 'Requirements',
        }
