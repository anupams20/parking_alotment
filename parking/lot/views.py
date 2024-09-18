from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserSignupForm, UserSigninForm
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import ParkingSpace,user,ParkingHistory
from .serializers import ParkingSpaceSerializers, ParkingHistorySerializer
import random
from datetime import datetime

def signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
           
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            
           
            user = User(username=username, email=email, first_name=name)
            user.set_password(password)
            user.save()

            
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home') 
    else:
        form = UserSignupForm()
    return render(request, 'lot/signup.html', {'form': form})

def signin(request):
    if request.method == 'POST':
        form = UserSigninForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Replace 'home' with your desired URL name after successful signin
            else:
                # Handle invalid credentials error
                form.add_error(None, "Invalid username or password. Please try again.")

    else:
        form = UserSigninForm()
    return render(request, 'lot/signin.html', {'form': form})

def homepage(request):
    return render(request, 'lot/home.html')

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Ensure user is authenticated
def parking_spaces(request):
    if request.user.role=="Admin":  # Admin check
        queryset = ParkingSpace.objects.all()
        serializer = ParkingSpaceSerializers(queryset, many=True)
        return Response(serializer.data)
    else:
        queryset = ParkingSpace.objects.all()
        spaces=[]
        for space in queryset:
            spaces.append({"level": space.level,
                        "twa": "Available" if space.twa > 0 else "Not Available",
                        "fwa": "Available" if space.fwa > 0 else "Not Available",
                    })
        return Response(spaces)
#-----------------------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def assign_parking(request):
    vehicle_category = request.data.get('vehicle_category')
    vehicle_number = request.data.get('vehicle_number')
    parking_level = request.data.get('parking_level')

    if not (vehicle_category and vehicle_number and parking_level):
        return Response({"error": "Missing required parameters."}, status=400)

    try:
        # Find a random available parking lot based on vehicle category and level
        if vehicle_category == '2-wheeler':
            available_spaces = ParkingSpace.objects.filter(Level=parking_level, TWA__gt=0)
        elif vehicle_category == '4-wheeler':
            available_spaces = ParkingSpace.objects.filter(Level=parking_level, FWA__gt=0)
        else:
            return Response({"error": "Invalid vehicle category."}, status=400)

        if not available_spaces.exists():
            return Response({"error": f"No available parking space for {vehicle_category} at level {parking_level}."}, status=400)

        random_space = random.choice(available_spaces)
        parking_s=ParkingSpace.objects.get(Level=parking_level)
        # Lock the parking space by updating availability
        if vehicle_category == '2-wheeler':
            parking_s.TWA -= 1
        elif vehicle_category == '4-wheeler':
            parking_s.FWA -= 1

        parking_s.save()

        # Record parking history
        now = datetime.now()
        parking_history = ParkingHistory.objects.create(
            Level=parking_level,
            Type='TW' if vehicle_category == '2-wheeler' else 'FW',
            VehicleNumber=vehicle_number,
            Lot=random_space.id,
            In=now,
            Fee=0  # Assuming fee calculation happens later
        )
        return Response({
            "vehicle_category": vehicle_category,
            "vehicle_number": vehicle_number,
            "parking_level": parking_level,
            "parking_lot_number": random_space.id,
            "locking_time": now,
            "user_id": request.user.id,
        })

    except Exception as e:
        return Response({"error": str(e)}, status=400)
#--------------------------------------------------------------------------------
@api_view(['POST'])
#@permission_classes([IsAuthenticated])
def unlock_parking(request):
    vehicle_number = request.data.get('vehicle_number')
    parking_lot_number = request.data.get('parking_lot_number')
    
    if not (vehicle_number and parking_lot_number):
        return Response({"error": "Vehicle number and parking lot number are required."}, status=400)
    try:
        parking_history = ParkingHistory.objects.get(Lot=parking_lot_number)
    except ParkingHistory.DoesNotExist:
        return Response({"error": f"Parking lot with ID {parking_lot_number} does not exist."}, status=404)
    parking_space=ParkingSpace.objects.get(Level=parking_history.Level)
    if parking_history.Type=='FW':
        parking_space.FWA+=1
    else:
        parking_space.TWA+=1
    parking_space.save()
    now = datetime.now()
    parking_history.Out = now

    parking_history.save()
    response_data = {
        "vehicle_number": vehicle_number,
        "parking_lot_number": parking_lot_number,
        "locking_time": parking_history.In,
        "unlocking_time": now,
        "parking_fee": 10*((now-parking_history.In)/3600),
        "user_id": request.user.id
    }

    return Response(response_data)