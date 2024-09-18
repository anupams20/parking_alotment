from django.db import models

class ParkingSpace(models.Model):
    id= models.AutoField(primary_key=True)
    Level=models.IntegerField()
    TWA=models.IntegerField()
    FWA=models.IntegerField()
    def __str__(self):
        return f"Level {self.Level} - TWA: {self.TWA}, FWA: {self.FWA}"



class user(models.Model):
    id= models.AutoField(primary_key=True)
    Name=models.CharField(max_length=30)
    Password=models.CharField(max_length=30)
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('PUBLIC', 'Public'),
    ]
    Role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='PUBLIC')

    def __str__(self):
        return self.Name

class ParkingHistory(models.Model):
    id=models.AutoField(primary_key=True)
    Level=models.IntegerField()
    Type=models.CharField(max_length=2)
    VehicleNumber=models.CharField(max_length=30)
    Lot=models.CharField(max_length=20)
    In=models.DateTimeField()
    Out=models.DateTimeField(null=True,blank=True)
    Fee=models.DecimalField(max_digits=5, decimal_places=2)
    def __str__(self):
        return f"{self.VehicleNumber} parked at {self.Lot} on Level {self.Level}"

