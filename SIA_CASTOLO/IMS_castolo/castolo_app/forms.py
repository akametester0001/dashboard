from django import forms
from .models import Animal  

class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = [
            'pet_name',
            'species',
            'breed',
            'date_of_birth',
            'date_of_adoption',
            'weight',
            'gender',
            'owner_name',
            'vaccination_status'
        ]
        widgets = {
            'pet_name': forms.TextInput(attrs={'class': 'form-control'}),
            'species': forms.Select(attrs={'class': 'form-control'}),
            'breed': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_of_adoption': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'owner_name': forms.TextInput(attrs={'class': 'form-control'}),
            'vaccination_status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }   