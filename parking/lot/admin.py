from django.contrib import admin
from .models import ParkingSpace, user, ParkingHistory
# Register your models here.
@admin.register(ParkingSpace)
class ParkingSpaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'Level', 'TWA', 'FWA')  # Display fields in admin list view
@admin.register(user)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'Name', 'Role')  # Display fields in admin list view
    list_filter = ('Role',)  # Add filters on Role field
@admin.register(ParkingHistory)
class ParkingHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'Level', 'Type', 'VehicleNumber', 'Lot', 'In', 'Out', 'Fee')  # Display fields in admin list view
    list_filter = ('Level', 'Type')  # Add filters on Level and Type fields
    search_fields = ('VehicleNumber', 'Lot')  # Add search functionality for VehicleNumber and Lot fields
    date_hierarchy = 'In'  # Add date-based drilldown navigation
