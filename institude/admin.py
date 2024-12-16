
from django.contrib import admin
from .models import Institute

# Helper function to get all fields dynamically
def get_all_field_names(model):
    return [field.name for field in model._meta.fields]

@admin.register(Institute)
class InstituteAdmin(admin.ModelAdmin):
    list_display = get_all_field_names(Institute)
    search_fields = ( 'email', )  # Add text fields suitable for search
