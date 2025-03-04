from django import forms
from .models import *
from django.core.exceptions import ValidationError
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password

class EmployeeCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')
    first_name = forms.CharField(max_length=100, label='First Name')
    last_name = forms.CharField(max_length=100, label='Last Name')
    gender = forms.ChoiceField(
        choices=[('male', 'Male'), ('female', 'Female')],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label="Gender",
    )
    phone = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'placeholder': 'Enter phone number'}))
    position = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Enter job position'}))
    department = forms.ModelChoiceField(
    queryset=Department.objects.exclude(name='ADMIN'),  # Exclude the department with name 'ADMIN'
    required=False,
    label="Department",
    empty_label="Select Department"
)

    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'gender', 'phone', 'position', 'department', 'start_date', 'role']

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords don't match.")
        return confirm_password

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError("This username already exists.")
        return username
