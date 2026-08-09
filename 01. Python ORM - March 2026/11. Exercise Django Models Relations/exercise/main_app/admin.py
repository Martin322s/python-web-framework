from django.contrib import admin
from main_app.models import Car

# Register your models here.
@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("model", "year", "owner", "car_details")

    @admin.display(description="Car Details")
    def car_details(self, obj):
        owner_name = obj.owner.name if obj.owner else "No owner"

        try:
            registration_number = obj.registration.registration_number
        except Car.registration.RelatedObjectDoesNotExist:
            registration_number = "No registration number"

        return f"Owner: {owner_name}, Registration: {registration_number}"