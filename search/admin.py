from django.contrib import admin
from .models import City

# Register the City model with the Django admin interface
@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Display the 'name' field in the list view
    search_fields = ('name',)  # Allow searching by the city name
    list_filter = ('name',)  # Optional: Filter cities by their name (in this case, it would be the same as the search)

