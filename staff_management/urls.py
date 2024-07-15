from django.urls import path
from .views import *

app_name = "staff_management"

urlpatterns = [
    path("", index, name="index"),
    path("tree/", EmployeeTreeView.as_view(), name="employee-tree"),
    path("load_subordinates/", load_subordinates, name="load-subordinates"),
    path("employees/", EmployeeListView.as_view(), name="employee-list"),
    ####### + CRUD HERE ###########

]

