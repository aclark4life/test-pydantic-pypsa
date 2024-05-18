# Register your models here.

from django.contrib import admin
from .models import EnergySystem

class EnergySystemAdmin(admin.ModelAdmin):
    # Display these fields in the admin list view
    list_display = ('name', 'capacity_mw', 'efficiency', 'cost_per_mw')
    # Add search capability to these fields
    search_fields = ('name',)
    # Enable filters for these fields
    list_filter = ('efficiency', 'cost_per_mw')

admin.site.register(EnergySystem, EnergySystemAdmin)
