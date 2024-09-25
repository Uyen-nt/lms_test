from django import forms
from .models import User, Role

# Form for creating and editing users
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'full_name', 'role']
        widgets = {
            'password': forms.PasswordInput(),
        }

# Form for creating and editing roles
class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['role_name']
