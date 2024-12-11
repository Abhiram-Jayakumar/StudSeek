from django.shortcuts import redirect, render

from Admin.models import District, Place

# Create your views here.

def admin_home(request):
    return render(request,'Admin/admin_home.html')


#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
def add_district(request):
    if request.method == 'POST':
        district_name = request.POST.get('district_name')
        if district_name:
            District.objects.create(District_name=district_name)
            return redirect('Admin:admin_home') 
    return render(request, 'Admin/add_district.html')

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def add_place(request):
    if request.method == 'POST':
        district_id = request.POST.get('district')
        place_name = request.POST.get('place_name')
        pincode = request.POST.get('pincode')

        if district_id and place_name and pincode:
            district = District.objects.get(id=district_id)
            Place.objects.create(District=district, Place_name=place_name, Pincode=pincode)
            return redirect('Admin:admin_home')  

    districts = District.objects.all()  
    return render(request, 'Admin/add_place.html', {'districts': districts})

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def List_loc(request):
    places = Place.objects.all()
    return render(request, 'Admin/List_of_loc.html', {'places': places})

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////