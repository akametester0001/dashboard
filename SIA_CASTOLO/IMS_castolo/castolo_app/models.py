from django.db import models


# Create your models here.

class Animal(models.Model):
    SPECIES_CHOICES = (
        ("Dog", "Dog"),
        ("Cat", "Cat"),
        ("Rabbit", "Rabbit"),
        ("Bird", "Bird"),
        ("Reptile", "Reptile"),
        ("Rat", "Rat"),
        ("Other", "Other"),
    )

    GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
    )

    pet_id = models.AutoField(primary_key=True)
    pet_name = models.CharField(max_length=100)
    species = models.CharField(
        max_length=100,
        choices=SPECIES_CHOICES
    )
    breed = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    date_of_adoption = models.DateField()
    weight = models.FloatField()
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )
    owner_name = models.CharField(max_length=100)
    vaccination_status = models.BooleanField(default=False)
    date_of_registration = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Pet ID: {self.pet_id}, Pet Name: {self.pet_name}, Species: {self.species}"