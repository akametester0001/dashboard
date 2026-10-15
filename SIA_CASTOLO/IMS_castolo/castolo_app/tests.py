from datetime import date

from django.test import TestCase
from django.urls import reverse

from .models import Animal


class AnimalDashboardTests(TestCase):
	def animal_data(self, **overrides):
		data = {
			'pet_name': 'Milo',
			'species': 'Dog',
			'breed': 'Mixed',
			'date_of_birth': '2022-01-15',
			'date_of_adoption': '2022-03-20',
			'weight': '12.5',
			'gender': 'Male',
			'owner_name': 'Alex Smith',
			'vaccination_status': 'on',
		}
		data.update(overrides)
		return data

	def test_dashboard_lists_animals(self):
		Animal.objects.create(
			pet_name='Milo',
			species='Dog',
			breed='Mixed',
			date_of_birth=date(2022, 1, 15),
			date_of_adoption=date(2022, 3, 20),
			weight=12.5,
			gender='Male',
			owner_name='Alex Smith',
			vaccination_status=True,
		)

		response = self.client.get(reverse('dashboard'))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Milo')

	def test_dashboard_creates_animal(self):
		response = self.client.post(reverse('dashboard'), self.animal_data())

		self.assertRedirects(response, reverse('dashboard'))
		self.assertEqual(Animal.objects.count(), 1)

	def test_animal_can_be_updated(self):
		animal = Animal.objects.create(
			pet_name='Milo',
			species='Dog',
			breed='Mixed',
			date_of_birth=date(2022, 1, 15),
			date_of_adoption=date(2022, 3, 20),
			weight=12.5,
			gender='Male',
			owner_name='Alex Smith',
		)

		response = self.client.post(
			reverse('animal_update', args=[animal.pk]),
			self.animal_data(pet_name='Milo Updated'),
		)

		self.assertRedirects(response, reverse('dashboard'))
		animal.refresh_from_db()
		self.assertEqual(animal.pet_name, 'Milo Updated')

	def test_animal_can_be_deleted(self):
		animal = Animal.objects.create(
			pet_name='Milo',
			species='Dog',
			breed='Mixed',
			date_of_birth=date(2022, 1, 15),
			date_of_adoption=date(2022, 3, 20),
			weight=12.5,
			gender='Male',
			owner_name='Alex Smith',
		)

		response = self.client.post(reverse('animal_delete', args=[animal.pk]))

		self.assertRedirects(response, reverse('dashboard'))
		self.assertFalse(Animal.objects.exists())
