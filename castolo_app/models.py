from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver


# Create your models here.

class Owner(models.Model):
    owner_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['full_name']

    def __str__(self):
        return self.full_name

    @property
    def pet_count(self):
        return self.pets.count()

    def delete(self, *args, **kwargs):
        # Only delete owner if no pets are linked
        if self.pets.exists():
            raise ValueError("Cannot delete owner with linked pets. Remove pets first.")
        super().delete(*args, **kwargs)


class Pet(models.Model):
    SPECIES_CHOICES = (
        ("Dog", "Dog"),
        ("Cat", "Cat"),
        ("Bird", "Bird"),
        ("Rabbit", "Rabbit"),
        ("Reptile", "Reptile"),
        ("Rat", "Rat"),
        ("Other", "Other"),
    )

    GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
    )

    VACCINATION_CHOICES = (
        ("Up to date", "Up to date"),
        ("Pending", "Pending"),
    )

    pet_id = models.AutoField(primary_key=True)
    pet_name = models.CharField(max_length=100)
    species = models.CharField(max_length=50, choices=SPECIES_CHOICES)
    breed = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    weight = models.DecimalField(max_digits=6, decimal_places=2)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    owner = models.ForeignKey(Owner, on_delete=models.PROTECT, related_name='pets')
    vaccination_status = models.CharField(max_length=20, choices=VACCINATION_CHOICES, default="Pending")
    date_registered = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_registered']

    def __str__(self):
        return f"Pet ID: {self.pet_id}, Name: {self.pet_name}, Species: {self.species}"

    @property
    def age(self):
        from datetime import date
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )


class Visit(models.Model):
    visit_id = models.AutoField(primary_key=True)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='visits')
    visit_date = models.DateField()
    reason = models.TextField()
    diagnosis = models.TextField(blank=True)
    treatment = models.TextField(blank=True)
    next_checkup_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-visit_date', '-visit_id']

    def __str__(self):
        return f"Visit #{self.visit_id} - {self.pet.pet_name} on {self.visit_date}"


@receiver(post_delete, sender=Pet)
def check_owner_empty(sender, instance, **kwargs):
    """Delete owner if no pets are linked after pet deletion"""
    owner = instance.owner
    if owner and not owner.pets.exists():
        owner.delete()