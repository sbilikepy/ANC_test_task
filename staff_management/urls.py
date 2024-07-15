from django.urls import path
from .views import *

app_name = "staff_management"

urlpatterns = [
    path("", index, name="index"),
    path("tree/", EmployeeTreeView.as_view(), name="employee-tree"),
    path("load_subordinates/", load_subordinates, name="load-subordinates"),
    path("employees/", EmployeeListView.as_view(), name="employee-list"),
    path(
        "load_employees/",
        load_employees_for_list_view,
        name="load-employees-for-list-view",
    ),
    # CRUD URLs
    path(
        "employees/create/",
        EmployeeCreateView.as_view(),
        name="employee-create"
    ),
    path(
        "employees/<int:pk>/update/",
        EmployeeUpdateView.as_view(),
        name="employee-update",
    ),
    path(
        "employees/<int:pk>/delete/",
        EmployeeDeleteView.as_view(),
        name="employee-delete",
    ),
    path(
        "employees/<int:pk>/",
        EmployeeDetailView.as_view(),
        name="employee-detail"
    ),
    path("employees/crud-info/", crud_info, name="employee-crud-info"),
]
