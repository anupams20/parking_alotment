from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('', views.homepage, name='home'),
    path('login/', views.signin, name='login1'),
    path('api/parking/assign', views.assign_parking, name='assign-parking'),
    path('api/parking_spaces/', views.parking_spaces, name='parking_spaces'),
    path('api/unlock/parking/', views.unlock_parking, name='unlock_parking'),
]