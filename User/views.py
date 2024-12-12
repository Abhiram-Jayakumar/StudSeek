from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from Admin.models import Admintable, District, Place
from User.models import BookingRoom, BusProvider, College, FoodVendor, Hostel, Providers, Room, User
from django.http import JsonResponse


# Create your views here.

def index(request):
    return render(request,'User/index.html')

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////

def user_reg(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        password = request.POST.get('password')

        if name and email and phone_number and address and password:
            User.objects.create(
                name=name,
                email=email,
                phone_number=phone_number,
                address=address,
                password=password  
            )
            messages.success(request, "User added successfully.")
            return redirect('User:index')  

    return render(request, 'User/User_registration.html')

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////

def register_provider(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        place_id = request.POST.get('place')
        email = request.POST.get('email')
        password = request.POST.get('password')

        place = Place.objects.get(id=place_id) if place_id else None

        if role and email and password:
            Providers.objects.create(
                role=role,
                phone_number=phone_number,
                address=address,
                place=place,
                email=email,
                password=password
            )
            messages.success(request, "Provider registered successfully.")
            return redirect('User:index')

    districts = District.objects.all()
    return render(request, 'User/register_provider.html', {'districts': districts, 'roles': Providers.ROLE_CHOICES})

def get_places_by_district(request, district_id):
    places = Place.objects.filter(District_id=district_id).values('id', 'Place_name')
    return JsonResponse(list(places), safe=False)

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def Bus_home(request):
    return render(request,'User/Bus_p_home.html')

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def College_home(request):
    return render(request,'User/College_home.html')

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def Food_v_home(request):
    return render(request,'User/Food_v_home.html')

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def Hostel_home(request):
    return render(request,'User/Hostel_home.html')

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


def Login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        provider = Providers.objects.filter(email=email, password=password).first()
        regular_user = User.objects.filter(email=email, password=password).first()
        admin = Admintable.objects.filter(email=email, password=password).first()
        if provider:
            request.session['provider_id'] = provider.id
            if provider.role == 'bus_service':
                return redirect('User:Bus_home')
            elif provider.role == 'food_vendor':
                return redirect('User:Food_v_home')
            elif provider.role == 'hostel':
                return redirect('User:Hostel_home')
            elif provider.role == 'college':
                return redirect('User:College_home')
        elif regular_user:
            request.session['user_id'] = regular_user.id
            return redirect('User:User_home')
        elif admin:
            request.session['admin_id'] = admin.id
            return redirect('Admin:admin_home')


        else:
            messages.error(request, "Invalid credentials. Please try again.")
            return render(request, "User/Login.html")

    return render(request, "User/Login.html")

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def reg_college_profile(request):
    if 'provider_id' not in request.session:
        messages.error(request, "You need to log in as a provider to register a hostel.")
        return redirect('User:login') 

    if request.method == 'POST':
        name = request.POST.get('name')
        district_id = request.POST.get('district')
        place_id = request.POST.get('place')
        address = request.POST.get('address')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        website = request.POST.get('website')
        loc = request.POST.get('loc')
        registered_by_id = request.session.get('provider_id')


        district = District.objects.get(id=district_id)
        place = Place.objects.get(id=place_id)
        registered_by = Providers.objects.get(id=registered_by_id) if registered_by_id else None


        College.objects.create(
            name=name,
            district=district,
            place=place,
            address=address,
            email=email,
            phone_number=phone_number,
            website=website,
            loc=loc,
            registered_by=registered_by

        )
        return redirect('User:index') 
    districts = District.objects.all()
    registered_by_id = request.session.get('provider_id')

    return render(request, 'User/reg_college_profile.html', {'districts': districts, 'registered_by_id': registered_by_id})

def get_places_by_district(request, district_id):
    places = Place.objects.filter(District_id=district_id).values('id', 'Place_name')
    return JsonResponse(list(places), safe=False)


#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def register_food_vendor(request):
    if 'provider_id' not in request.session:
        messages.error(request, "You need to log in as a provider to register a food vendor.")
        return redirect('User:login') 

    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            district_id = request.POST.get('district')
            place_id = request.POST.get('place')
            address = request.POST.get('address')
            email = request.POST.get('email')
            phone_number = request.POST.get('phone_number')
            website = request.POST.get('website')
            loc = request.POST.get('loc')
            registered_by_id = request.session.get('provider_id')

            district = District.objects.get(id=district_id)
            place = Place.objects.get(id=place_id)
            registered_by = Providers.objects.get(id=registered_by_id) if registered_by_id else None

            if name and email:
                FoodVendor.objects.create(
                    name=name,
                    district=district,
                    place=place,
                    address=address,
                    email=email,
                    phone_number=phone_number,
                    website=website,
                    loc=loc,
                    registered_by=registered_by
                )
                messages.success(request, "Food Vendor registered successfully.")
                return redirect('User:Food_v_home')  

        except District.DoesNotExist:
            messages.error(request, "Invalid district selected.")
        except Place.DoesNotExist:
            messages.error(request, "Invalid place selected.")
        except Providers.DoesNotExist:
            messages.error(request, "Invalid provider. Please log in again.")

    districts = District.objects.all()
    registered_by_id = request.session.get('provider_id')
    return render(request, 'User/register_food_vendor.html', {'districts': districts, 'registered_by_id': registered_by_id})


#////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def register_hostel_profile(request):
    if 'provider_id' not in request.session:
        messages.error(request, "You need to log in as a provider to register a hostel.")
        return redirect('User:login') 

    if request.method == 'POST':
        name = request.POST.get('name')
        district_id = request.POST.get('district')
        place_id = request.POST.get('place')
        address = request.POST.get('address')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        website = request.POST.get('website')
        loc = request.POST.get('loc')
        registered_by_id = request.session.get('provider_id')

        district = District.objects.get(id=district_id) if district_id else None
        place = Place.objects.get(id=place_id) if place_id else None
        registered_by = Providers.objects.get(id=registered_by_id) if registered_by_id else None

        if name and district and place and email and phone_number and registered_by:
            Hostel.objects.create(
                name=name,
                district=district,
                place=place,
                address=address,
                email=email,
                phone_number=phone_number,
                website=website,
                loc=loc,
                registered_by=registered_by
            )
            messages.success(request, "Hostel registered successfully.")
            return redirect('User:index')  
        else:
            messages.error(request, "Please fill in all required fields.")

    districts = District.objects.all()
    registered_by_id = request.session.get('provider_id')
    return render(request, 'User/register_hostel_profile.html', {'districts': districts, 'registered_by_id': registered_by_id})

def get_places_by_district(request, district_id):
    places = Place.objects.filter(District_id=district_id).values('id', 'Place_name')
    return JsonResponse(list(places), safe=False)


#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def register_bus_provider(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        district_id = request.POST.get('district')
        place_id = request.POST.get('place')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        website = request.POST.get('website')
        route_details = request.POST.get('route_details')
        
        registered_by_id = request.session.get('provider_id')  
        registered_by = Providers.objects.get(id=registered_by_id) if registered_by_id else None

        if name and district_id and place_id and address and phone_number and email:
            district = District.objects.get(id=district_id)
            place = Place.objects.get(id=place_id)
            BusProvider.objects.create(
                name=name,
                district=district,
                place=place,
                address=address,
                phone_number=phone_number,
                email=email,
                website=website,
                route_details=route_details,
                registered_by=registered_by
            )
            messages.success(request, 'Bus provider registered successfully.')
            return redirect('User:index')  
        else:
            messages.error(request, 'Please fill in all required fields.')

    districts = District.objects.all()
    providers = Providers.objects.all()  
    return render(request, 'User/register_bus_provider.html', {'districts': districts, 'providers': providers})


#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def view_bus_provider_profile(request):
    provider_id = request.session.get('provider_id') 

    if not provider_id:
        return redirect('User:login')  

    bus_provider = get_object_or_404(BusProvider, registered_by_id=provider_id)

    return render(request, 'User/view_bus_provider_profile.html', {'bus_provider': bus_provider})

#//////////////////////////////////////////////////////////////////////////////////////////////////////////

def view_food_vendor_profile(request):
    provider_id = request.session.get('provider_id')  

    if not provider_id:
        return redirect('User:login') 
    food_vendor = get_object_or_404(FoodVendor, registered_by_id=provider_id)

    return render(request, 'User/view_food_vendor_profile.html', {'food_vendor': food_vendor})

#//////////////////////////////////////////////////////////////////////////////////////////////////////////

def view_hostel_profile(request):
    provider_id = request.session.get('provider_id')  

    if not provider_id:
        return redirect('User:login')  

    hostel = get_object_or_404(Hostel, registered_by_id=provider_id)

    return render(request, 'User/view_hostel_profile.html', {'hostel': hostel})

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def view_college_profile(request):
    provider_id = request.session.get('provider_id')  

    if not provider_id:
        return redirect('User:login')  

    college = get_object_or_404(College, registered_by_id=provider_id) 

    return render(request, 'User/view_college_profile.html', {'college': college})

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def User_home(request):
    districts = District.objects.all()
    places = Place.objects.all()
    results = {
        'colleges': [],
        'food_vendors': [],
        'hostels': [],
        'bus_providers': [],
        'room':[],
    }

    if request.method == 'POST':
        district_id = request.POST.get('district')
        place_id = request.POST.get('place')

        

        results['colleges'] = College.objects.filter(district_id=district_id)
        results['food_vendors'] = FoodVendor.objects.filter(district_id=district_id)
        results['hostels'] = Hostel.objects.filter(district_id=district_id,)
        results['bus_providers'] = BusProvider.objects.filter(district_id=district_id)
        results['hostels'] = Hostel.objects.filter(district_id=district_id).prefetch_related('rooms')

       

        if place_id:
            results['colleges'] = results['colleges'].filter(place_id=place_id)
            results['food_vendors'] = results['food_vendors'].filter(place_id=place_id)
            results['hostels'] = results['hostels'].filter(place_id=place_id)
            results['bus_providers'] = results['bus_providers'].filter(place_id=place_id)
            
    return render(request, 'User/User_home.html', {
        'districts': districts,
        'places': places,
        'results': results,
        
    })

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def add_room(request):
    provider_id = request.session.get('provider_id')  
    if provider_id is None:
        messages.error(request, "You need to log in as a provider to register a hostel.")
        return redirect('User:login') 

    if request.method == 'POST':
        room_number = request.POST.get('room_number')
        capacity = request.POST.get('capacity')
        rent_amount = request.POST.get('Rent_amount')
        is_available = request.POST.get('is_available') == 'True' 
        description = request.POST.get('description')

        provider = Providers.objects.get(id=provider_id)
        if provider:
            hostel = provider.hostel_set.first() 

            if hostel:
                Room.objects.create(
                    hostel=hostel,
                    room_number=room_number,
                    capacity=capacity,
                    Rent_amount=rent_amount,
                    is_available=is_available,
                    description=description
                )
                return redirect('User:Hostel_home')
            else:
                messages.error(request, "No associated hostel found.")
                return redirect('User:add_room')

    hostels = Hostel.objects.all() 
    return render(request, 'User/Hostel_add_room.html', {'hostels': hostels, 'hostel': provider_id})

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////


def hostel_details(request, hostel_id):
    hostel = get_object_or_404(Hostel, id=hostel_id)
    rooms = hostel.rooms.filter(is_available=True)
    
    if request.method == 'POST':
        room_id = request.POST.get('room_id')
        selected_room = get_object_or_404(Room, id=room_id)
        chosen_capacity = int(request.POST.get('capacity'))
        check_in_date = request.POST.get('check_in_date')
        special_requests = request.POST.get('special_requests')
        amount = selected_room.Rent_amount
        
        user_id = request.session.get('user_id')
        if user_id is not None:  
            booking = BookingRoom(
                user_id=user_id, 
                room=selected_room,
                capacity=chosen_capacity,
                amount=amount,
                check_in_date=check_in_date,
                special_requests=special_requests
            )
            booking.save()
            return redirect('User:User_home')  
        else:
            return render(request, 'User/Login.html', {'message': 'User is not logged in.'})

    return render(request, 'User/view_hostel_room_details.html', {
        'hostel': hostel,
        'rooms': rooms,
    })

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def user_booking_records(request):
    user_id = request.session.get('user_id')  

    if user_id:
        bookings = BookingRoom.objects.filter(user_id=user_id).order_by('-booking_date')
    else:
        bookings = []  

    return render(request, 'User/user_booking_records.html', {
        'bookings': bookings,
    })

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


def view_bookings_for_hostel(request):
    provider_id = request.session.get('provider_id')
    if not provider_id:
        return redirect('User:Login')  

    rooms_owned = Room.objects.filter(hostel__registered_by_id=provider_id)
    bookings = BookingRoom.objects.filter(room__in=rooms_owned)

    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        booking = get_object_or_404(BookingRoom, id=booking_id)
        booking.booking_status = 'confirmed'
        booking.rental_service_approval_status = True
        booking.save()
        return redirect('User:view_bookings_for_hostel') 
    return render(request, 'User/hostel_bookings.html', {
        'bookings': bookings,
    })

#////////////////////////////////////////////////////////////////////////////////////////////////////////

def payment(request, booking_id):
    booking = get_object_or_404(BookingRoom, id=booking_id)

    if request.method == 'POST':
        booking.payment = True
        booking.save()
        messages.success(request, 'Payment processed successfully!')
        return redirect('User:user_booking_records') 

    return render(request, 'User/payment.html', {'booking': booking})