from django import forms
from django.forms import ModelForm
from applications.security.models import GroupModulePermission
from django.contrib.auth.models import Group
from applications.security.models import Module

class GroupModulePermissionForm(ModelForm):
    
    class Meta:
        model = GroupModulePermission
        fields = ['group', 'module']
        
        widgets = {
            'group': forms.Select(attrs={
                'class': 'form-control',
                'style': 'display: none;'  # Oculto porque se maneja con JavaScript
            }),
            'module': forms.Select(attrs={
                'class': 'form-control',
                'style': 'display: none;'  # Oculto porque se maneja con JavaScript
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Los campos no son requeridos porque se manejan dinámicamente
        self.fields['group'].required = False
        self.fields['module'].required = False