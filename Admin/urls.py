from django.urls import path
from Admin import views


app_name='Admin'

urlpatterns=[
    path('admin_home/',views.admin_home,name='admin_home'),
    path('add-district/',views.add_district, name='add_district'),
    path('add-place/',views.add_place, name='add_place'),
    path('List_loc/',views.List_loc, name='List_loc'),

]