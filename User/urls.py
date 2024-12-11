from django.urls import path
from User import views


app_name='User'
urlpatterns=[

    path('index/',views.index,name='index'),
    path('user_reg/',views.user_reg, name='user_reg'),
    path('register_provider/', views.register_provider, name='register_provider'),
    path('get-places/<int:district_id>/', views.get_places_by_district, name='get_places_by_district'),
    path('Bus_home/',views.Bus_home,name='Bus_home'),
    path('Hostel_home/',views.Hostel_home,name='Hostel_home'),
    path('Food_v_home/',views.Food_v_home,name='Food_v_home'),
    path('College_home/',views.College_home,name='College_home'),
    path('User_home/',views.User_home,name='User_home'),
    path('login/', views.Login, name='login'), 
    path('reg_college_profile/', views.reg_college_profile, name='reg_college_profile'),
    path('register_food_vendor/', views.register_food_vendor, name='register_food_vendor'),
    path('register_hostel_profile/', views.register_hostel_profile, name='register_hostel_profile'),
    path('register_bus_provider/', views.register_bus_provider, name='register_bus_provider'),
    path('view_bus_provider_profile/', views.view_bus_provider_profile, name='view_bus_provider_profile'),
    path('view_food_vendor_profile/', views.view_food_vendor_profile, name='view_food_vendor_profile'),
    path('view_hostel_profile/', views.view_hostel_profile, name='view_hostel_profile'),
    path('view_college_profile/', views.view_college_profile, name='view_college_profile'),
    path('add_room/',views.add_room, name='add_room'),
    path('hostel/<int:hostel_id>/details/',views. hostel_details, name='hostel_details'),
    path('booking-records/', views.user_booking_records, name='user_booking_records'),
    path('hostel-bookings/', views.view_bookings_for_hostel, name='view_bookings_for_hostel'),
    path('payment/<int:booking_id>/', views.payment, name='payment'),
    
    ]