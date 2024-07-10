from .views import *
from django.urls import path


app_name = "staff_management"

urlpatterns = [

    path("", index, name="index"),
    path("tree/", EmployeeTreeView.as_view(), name="employee-tree"),
    path("employees/", EmployeeListView.as_view(), name="employee-list"),


]
