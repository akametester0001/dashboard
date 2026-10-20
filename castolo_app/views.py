from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.db.models import Count, Q
from django.contrib import messages
from datetime import date

from .forms import OwnerForm, PetForm, VisitForm
from .models import Owner, Pet, Visit


# =============================================================================
# Dashboard
# =============================================================================

def dashboard(request):
    """Main dashboard with overview statistics for pets, owners, and visits."""
    total_pets = Pet.objects.count()
    total_owners = Owner.objects.count()
    total_visits = Visit.objects.count()
    
    # Vaccination stats
    vaccinated_pets = Pet.objects.filter(vaccination_status="Up to date").count()
    pending_vaccination = Pet.objects.filter(vaccination_status="Pending").count()
    
    # Vaccination rate
    vaccination_rate = 0
    if total_pets > 0:
        vaccination_rate = round((vaccinated_pets / total_pets) * 100)
    
    # Recent activity
    recent_pets = Pet.objects.select_related('owner').order_by('-date_registered')[:5]
    recent_visits = Visit.objects.select_related('pet', 'pet__owner').order_by('-visit_date', '-visit_id')[:5]
    
    # Species distribution for chart
    species_data = Pet.objects.values('species').annotate(count=Count('species')).order_by('-count')
    species_dict = {item['species']: item['count'] for item in species_data}
    
    context = {
        'total_pets': total_pets,
        'total_owners': total_owners,
        'total_visits': total_visits,
        'vaccinated_pets': vaccinated_pets,
        'pending_vaccination': pending_vaccination,
        'vaccination_rate': vaccination_rate,
        'recent_pets': recent_pets,
        'recent_visits': recent_visits,
        'species_data': species_dict,
    }
    return render(request, 'pawtrack/dashboard.html', context)


def index(request):
    """Legacy redirect to dashboard."""
    return redirect('dashboard')


# =============================================================================
# Owner Views
# =============================================================================

def owner_list(request):
    """List all owners with search functionality."""
    query = request.GET.get('q', '')
    owners = Owner.objects.prefetch_related('pets').order_by('full_name')
    
    if query:
        owners = owners.filter(
            Q(full_name__icontains=query) |
            Q(contact_number__icontains=query) |
            Q(email__icontains=query)
        )
    
    return render(request, 'pawtrack/owner_list.html', {
        'owners': owners,
        'query': query,
    })


def owner_create(request):
    """Create a new owner."""
    if request.method == 'POST':
        form = OwnerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Owner registered successfully!')
            return redirect('owner_list')
    else:
        form = OwnerForm()
    return render(request, 'pawtrack/owner_form.html', {'form': form, 'title': 'Register Owner'})


def owner_detail(request, pk):
    """View owner details and their pets."""
    owner = get_object_or_404(Owner, pk=pk)
    pets = owner.pets.all().order_by('-date_registered')
    return render(request, 'pawtrack/owner_detail.html', {'owner': owner, 'pets': pets})


def owner_update(request, pk):
    """Update owner details."""
    owner = get_object_or_404(Owner, pk=pk)
    if request.method == 'POST':
        form = OwnerForm(request.POST, instance=owner)
        if form.is_valid():
            form.save()
            messages.success(request, 'Owner updated successfully!')
            return redirect('owner_detail', pk=owner.pk)
    else:
        form = OwnerForm(instance=owner)
    return render(request, 'pawtrack/owner_form.html', {
        'form': form,
        'title': f'Edit {owner.full_name}',
        'editing_owner': owner
    })


@require_POST
def owner_delete(request, pk):
    """Delete an owner (only if no pets are linked)."""
    owner = get_object_or_404(Owner, pk=pk)
    try:
        owner.delete()
        messages.success(request, 'Owner deleted successfully!')
    except ValueError as e:
        messages.error(request, str(e))
    return redirect('owner_list')


# =============================================================================
# Pet Views
# =============================================================================

def pet_list(request):
    """List all pets with search and filter functionality."""
    query = request.GET.get('q', '')
    species_filter = request.GET.get('species', '')
    vaccination_filter = request.GET.get('vaccination', '')
    
    pets = Pet.objects.select_related('owner').order_by('-date_registered')
    
    if query:
        pets = pets.filter(
            Q(pet_name__icontains=query) |
            Q(owner__full_name__icontains=query) |
            Q(breed__icontains=query)
        )
    if species_filter:
        pets = pets.filter(species=species_filter)
    if vaccination_filter:
        pets = pets.filter(vaccination_status=vaccination_filter)
    
    species_choices = Pet.SPECIES_CHOICES
    vaccination_choices = Pet.VACCINATION_CHOICES
    
    return render(request, 'pawtrack/pet_list.html', {
        'pets': pets,
        'query': query,
        'species_filter': species_filter,
        'vaccination_filter': vaccination_filter,
        'species_choices': species_choices,
        'vaccination_choices': vaccination_choices,
    })


def pet_create(request):
    """Create a new pet (and optionally a new owner)."""
    if request.method == 'POST':
        form = PetForm(request.POST)
        if form.is_valid():
            pet = form.save()
            messages.success(request, f'{pet.pet_name} registered successfully!')
            return redirect('pet_list')
    else:
        form = PetForm()
    return render(request, 'pawtrack/pet_form.html', {'form': form, 'title': 'Register Pet'})


def pet_detail(request, pk):
    """View pet details and visit history."""
    pet = get_object_or_404(Pet.objects.select_related('owner'), pk=pk)
    visits = pet.visits.all().order_by('-visit_date', '-visit_id')
    return render(request, 'pawtrack/pet_detail.html', {'pet': pet, 'visits': visits})


def pet_update(request, pk):
    """Update pet details."""
    pet = get_object_or_404(Pet, pk=pk)
    if request.method == 'POST':
        form = PetForm(request.POST, instance=pet)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pet updated successfully!')
            return redirect('pet_detail', pk=pet.pk)
    else:
        form = PetForm(instance=pet)
    return render(request, 'pawtrack/pet_form.html', {
        'form': form,
        'title': f'Edit {pet.pet_name}',
        'editing_pet': pet
    })


@require_POST
def pet_delete(request, pk):
    """Delete a pet record."""
    pet = get_object_or_404(Pet, pk=pk)
    pet_name = pet.pet_name
    pet.delete()
    messages.success(request, f'{pet_name} deleted successfully!')
    return redirect('pet_list')


# =============================================================================
# Visit Views
# =============================================================================

def visit_list(request):
    """List all visits with search and filter."""
    query = request.GET.get('q', '')
    pet_filter = request.GET.get('pet', '')
    
    visits = Visit.objects.select_related('pet', 'pet__owner').order_by('-visit_date', '-visit_id')
    
    if query:
        visits = visits.filter(
            Q(pet__pet_name__icontains=query) |
            Q(reason__icontains=query) |
            Q(diagnosis__icontains=query)
        )
    if pet_filter:
        visits = visits.filter(pet_id=pet_filter)
    
    pets = Pet.objects.all().order_by('pet_name')
    
    return render(request, 'pawtrack/visit_list.html', {
        'visits': visits,
        'query': query,
        'pet_filter': pet_filter,
        'pets': pets,
    })


def visit_create(request):
    """Create a new visit/checkup record."""
    if request.method == 'POST':
        form = VisitForm(request.POST)
        if form.is_valid():
            visit = form.save()
            messages.success(request, 'Visit recorded successfully!')
            return redirect('visit_list')
    else:
        # Pre-select pet if provided in query string
        pet_id = request.GET.get('pet')
        initial = {}
        if pet_id:
            initial['pet'] = pet_id
        form = VisitForm(initial=initial)
    return render(request, 'pawtrack/visit_form.html', {'form': form, 'title': 'Record Visit'})


def visit_detail(request, pk):
    """View visit details."""
    visit = get_object_or_404(Visit.objects.select_related('pet', 'pet__owner'), pk=pk)
    return render(request, 'pawtrack/visit_detail.html', {'visit': visit})


def visit_update(request, pk):
    """Update visit details."""
    visit = get_object_or_404(Visit, pk=pk)
    if request.method == 'POST':
        form = VisitForm(request.POST, instance=visit)
        if form.is_valid():
            form.save()
            messages.success(request, 'Visit updated successfully!')
            return redirect('visit_detail', pk=visit.pk)
    else:
        form = VisitForm(instance=visit)
    return render(request, 'pawtrack/visit_form.html', {
        'form': form,
        'title': f'Edit Visit #{visit.visit_id}',
        'editing_visit': visit
    })


@require_POST
def visit_delete(request, pk):
    """Delete a visit record."""
    visit = get_object_or_404(Visit, pk=pk)
    visit.delete()
    messages.success(request, 'Visit deleted successfully!')
    return redirect('visit_list')