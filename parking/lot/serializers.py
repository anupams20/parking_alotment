from rest_framework import serializers
from .models import ParkingSpace, User, ParkingHistory

class ParkingSpaceSerializers(serializers.ModelSerializer):
    class Meta:
        model=ParkingSpace
        fields=('ID', 'Level', 'TWA', 'FWA')

class ParkingHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingHistory
        fields = ('id', 'Level', 'Type', 'VehicleNumber', 'Lot', 'In', 'Out', 'Fee')
