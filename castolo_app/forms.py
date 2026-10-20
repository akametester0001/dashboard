from datetime import date
from django import forms
from .models import Owner, Pet, Visit


class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ['full_name', 'contact_number', 'email', 'address']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Address'}),
        }


class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = [
            'pet_name',
            'species',
            'breed',
            'date_of_birth',
            'weight',
            'gender',
            'owner',
            'vaccination_status',
        ]
        widgets = {
            'pet_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pet Name'}),
            'species': forms.Select(attrs={'class': 'form-control'}),
            'breed': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Breed'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'placeholder': 'Weight (kg)'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'owner': forms.Select(attrs={'class': 'form-control'}),
            'vaccination_status': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Order owners by name for better UX
        self.fields['owner'].queryset = Owner.objects.order_by('full_name')
        self.fields['owner'].empty_label = "Select an owner..."


class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = [
            'pet',
            'visit_date',
            'reason',
            'diagnosis',
            'treatment',
            'next_checkup_date',
        ]
        widgets = {
            'pet': forms.Select(attrs={'class': 'form-control'}),
            'visit_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Reason for visit'}),
            'diagnosis': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Diagnosis'}),
            'treatment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Treatment given'}),
            'next_checkup_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Order pets by name for better UX
        self.fields['pet'].queryset = Pet.objects.select_related('owner').order_by('pet_name')
        self.fields['pet'].empty_label = "Select a pet..."
        # Set default visit date to today
        if not self.instance.pk:
            self.fields['visit_date'].initial = date.today()