from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import AnimalForm
from .models import Animal


def index(request):
       if request.method == 'POST':
              animal_form = AnimalForm(request.POST)
              if animal_form.is_valid():
                     animal_form.save()
                     return redirect('dashboard')
       else:
              animal_form = AnimalForm()

       return render(request, 'inventory/dashboard.html', {
              'animals': Animal.objects.all().order_by('-date_of_registration', '-pet_id'),
              'animal_form': animal_form,
       })


def animal_update(request, pk):
       animal = get_object_or_404(Animal, pk=pk)
       if request.method == 'POST':
              animal_form = AnimalForm(request.POST, instance=animal)
              if animal_form.is_valid():
                     animal_form.save()
                     return redirect('dashboard')
       else:
              animal_form = AnimalForm(instance=animal)

       return render(request, 'inventory/dashboard.html', {
              'animals': Animal.objects.all().order_by('-date_of_registration', '-pet_id'),
              'animal_form': animal_form,
              'editing_animal': animal,
       })


@require_POST
def animal_delete(request, pk):
       animal = get_object_or_404(Animal, pk=pk)
       animal.delete()
       return redirect('dashboard')