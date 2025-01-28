from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.core.exceptions import ValidationError

# National ID validation function
def national_code_checker(string):
    if not string.isdigit() or len(string) != 10:  # Ensure it's exactly 10 digits
        raise ValidationError("National ID must be a 10-digit number.")

    total = sum(int(string[i]) * (len(string) - i) for i in range(len(string) - 1))
    
    check_digit = int(string[-1])
    remainder = total % 11
    
    if remainder < 2:
        valid = check_digit == remainder
    else:
        valid = check_digit == (11 - remainder)
    
    if not valid:
        raise ValidationError("Invalid National ID.")

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.core.exceptions import ValidationError

# National ID validation function
def national_code_checker(string):
    if not string.isdigit() or len(string) != 10:  # Ensure it's exactly 10 digits
        raise ValidationError("National ID must be a 10-digit number.")

    total = sum(int(string[i]) * (len(string) - i) for i in range(len(string) - 1))
    
    check_digit = int(string[-1])
    remainder = total % 11
    
    if remainder < 2:
        valid = check_digit == remainder
    else:
        valid = check_digit == (11 - remainder)
    
    if not valid:
        raise ValidationError("Invalid National ID.")

class CustomUserForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15, required=True)
    national_id = forms.CharField(max_length=10, required=True)
    student_id = forms.CharField(max_length=20, required=False)
    is_admin = forms.BooleanField(required=False)
    admin_code = forms.CharField(max_length=20, required=False, help_text="Enter your admin code.")

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'national_id', 'student_id', 'is_admin', 'admin_code', 'password1', 'password2']

    def clean_national_id(self):
        national_id = self.cleaned_data.get("national_id")
        national_code_checker(national_id)
        return national_id

    def clean(self):
        cleaned_data = super().clean()
        is_admin = cleaned_data.get("is_admin")
        student_id = cleaned_data.get("student_id")
        admin_code = cleaned_data.get("admin_code")

        if is_admin:
            if not admin_code:
                raise forms.ValidationError("Admins must enter an admin code.")
            cleaned_data["student_id"] = None  # Ensure no student_id is saved
        else:
            if not student_id:
                raise forms.ValidationError("Students must enter a Student ID.")
            cleaned_data["admin_code"] = None  # Ensure no admin_code is saved for students

        return cleaned_data
