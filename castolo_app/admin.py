from django.contrib import admin
from .models import Owner, Pet, Visit


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ['owner_id', 'full_name', 'contact_number', 'email', 'pet_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['full_name', 'contact_number', 'email', 'address']
    ordering = ['full_name']
    readonly_fields = ['created_at', 'updated_at']
    
    def pet_count(self, obj):
        return obj.pet_count
    pet_count.short_description = 'Pets'


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ['pet_id', 'pet_name', 'species', 'breed', 'owner', 'gender', 'weight', 'vaccination_status', 'date_registered']
    list_filter = ['species', 'gender', 'vaccination_status', 'date_registered']
    search_fields = ['pet_name', 'breed', 'owner__full_name']
    ordering = ['-date_registered']
    readonly_fields = ['date_registered']
    list_select_related = ['owner']


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ['visit_id', 'pet', 'visit_date', 'reason', 'diagnosis', 'next_checkup_date']
    list_filter = ['visit_date', 'pet__species']
    search_fields = ['pet__pet_name', 'reason', 'diagnosis', 'treatment']
    ordering = ['-visit_date', '-visit_id']
    readonly_fields = ['created_at', 'updated_at']
    list_select_related = ['pet', 'pet__owner']
    date_hierarchy = 'visit_date'