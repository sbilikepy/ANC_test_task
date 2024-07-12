from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.http import JsonResponse, HttpRequest, HttpResponse

from django.shortcuts import render
from django.views import View
from .models import Employee, Position


def index(request):
    return render(
        request,
        template_name="staff_management/index.html",
        context={
            "db_size": Employee.objects.count(),

            "lvl_7": Employee.objects.filter(
                position__hierarchy_level=7).count(),

            "lvl_6": Employee.objects.filter(
                position__hierarchy_level=6).count(),

            "lvl_5": Employee.objects.filter(
                position__hierarchy_level=5).count(),

            "lvl_4": Employee.objects.filter(
                position__hierarchy_level=4).count(),

            "lvl_3": Employee.objects.filter(
                position__hierarchy_level=3).count(),

            "lvl_2": Employee.objects.filter(
                position__hierarchy_level=2).count(),

            "lvl_1": Employee.objects.filter(
                position__hierarchy_level=1).count(),

        },
    )


class EmployeeTreeView(generic.ListView):  # TODO: LoginRequiredMixin later
    model = Employee
    context_object_name = "employees_tree"
    template_name = "staff_management/employee/employee_tree.html"



class EmployeeListView(LoginRequiredMixin, generic.ListView): # TODO: LoginRequiredMixin later
    model = Employee
    context_object_name = "employee_list"
    template_name = "staff_management/employee/employee_list.html"

