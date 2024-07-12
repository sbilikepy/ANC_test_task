from . import views
from .views import *
from django.urls import path

app_name = "staff_management"

urlpatterns = [

    path("", index, name="index"),

    path("tree/", EmployeeTreeView.as_view(), name="employee-tree"),
    path('load_subordinates/', views.load_subordinates,
         name='load-subordinates'),

    path("employees/", EmployeeListView.as_view(), name="employee-list"),
    ####### + CRUD HERE ###########

]

