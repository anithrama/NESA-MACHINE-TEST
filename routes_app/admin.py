from django.contrib import admin

from .models import AirportRoute


@admin.register(AirportRoute)
class AirportRouteAdmin(admin.ModelAdmin):
	list_display = ("airport_code", "position", "direction", "duration")
	list_filter = ("direction", "position")
	search_fields = ("airport_code",)
	ordering = ("position",)
