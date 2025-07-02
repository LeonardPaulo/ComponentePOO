from django import forms
from applications.security.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'dni', 'username', 'email', 'first_name', 'last_name',
            'image', 'direction', 'phone', 'is_active', 'is_staff', 'is_superuser'
        ]
        widgets = {
            'image': forms.FileInput(attrs={
                'accept': 'image/*',
                'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent text-gray-700 bg-white'
            }),
            'direction': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Ingrese la dirección completa'
            }),
        }