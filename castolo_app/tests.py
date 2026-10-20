from datetime import date

from django.test import TestCase
from django.urls import reverse

from .models import Owner, Pet, Visit


class PawTrackTests(TestCase):
    def setUp(self):
        self.owner = Owner.objects.create(
            full_name="Alex Smith",
            contact_number="555-0100",
            email="alex@example.com",
            address="1 Main Street",
        )
        self.pet = Pet.objects.create(
            pet_name="Milo",
            species="Dog",
            breed="Mixed",
            date_of_birth=date(2022, 1, 15),
            weight=12.5,
            gender="Male",
            owner=self.owner,
            vaccination_status="Up to date",
        )

    def test_dashboard_lists_pets(self):
        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Milo")

    def test_owner_can_be_created(self):
        response = self.client.post(
            reverse("owner_create"),
            {
                "full_name": "Jamie Lee",
                "contact_number": "555-0101",
                "email": "jamie@example.com",
                "address": "2 Main Street",
            },
        )

        self.assertRedirects(response, reverse("owner_list"))
        self.assertTrue(Owner.objects.filter(full_name="Jamie Lee").exists())

    def test_pet_can_be_created(self):
        response = self.client.post(
            reverse("pet_create"),
            {
                "pet_name": "Luna",
                "species": "Cat",
                "breed": "Domestic shorthair",
                "date_of_birth": "2023-05-10",
                "weight": "4.25",
                "gender": "Female",
                "owner": self.owner.pk,
                "vaccination_status": "Pending",
            },
        )

        self.assertRedirects(response, reverse("pet_list"))
        self.assertTrue(Pet.objects.filter(pet_name="Luna").exists())

    def test_visit_can_be_recorded(self):
        response = self.client.post(
            reverse("visit_create"),
            {
                "pet": self.pet.pk,
                "visit_date": date.today().isoformat(),
                "reason": "Annual checkup",
                "diagnosis": "",
                "treatment": "",
                "next_checkup_date": "",
            },
        )

        self.assertRedirects(response, reverse("visit_list"))
        self.assertTrue(Visit.objects.filter(pet=self.pet, reason="Annual checkup").exists())
