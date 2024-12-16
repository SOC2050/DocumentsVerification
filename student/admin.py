
# Register your models here.
from django.contrib import admin
from .models import StudentDetails, StudentCredentials , StudentDocuments

# Helper function to get all fields dynamically
def get_all_field_names(model):
    return [field.name for field in model._meta.fields]

@admin.register(StudentDetails)
class StudentDetailsAdmin(admin.ModelAdmin):
    list_display = get_all_field_names(StudentDetails)
    search_fields = ('applicationId', 'email__email')  # Add text fields suitable for search

@admin.register(StudentCredentials)
class StudentCredentialsAdmin(admin.ModelAdmin):
    list_display = get_all_field_names(StudentCredentials)
    search_fields = ('email',)  # Add text fields suitable for search


@admin.register(StudentDocuments)
class StudentDocumentsAdmin( admin.ModelAdmin):
    list_display = get_all_field_names(StudentDocuments) 
    search_fields = ('email',)