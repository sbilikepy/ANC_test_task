from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views import generic
from django.http import JsonResponse, HttpRequest, HttpResponse

from django.shortcuts import render
from django.views import View

from .forms import EmployeeSearchForm
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


class EmployeeTreeView(View):
    def get(self, request):
        employees = Employee.objects.all()
        levels = range(1, 8)  # Levels from 1 to 7
        return render(request,
                      'staff_management/employee/employee_tree.html',
                      {'employees': employees, 'levels': levels})


def load_subordinates(request):
    employee_id = request.GET.get('employee_id')

    try:
        employee = Employee.objects.get(id=employee_id)
    except Employee.DoesNotExist:
        return JsonResponse({'error': 'Employee not found'}, status=404)

    subordinates = Employee.objects.filter(
        supervisor=employee.id
    ).values('id', 'full_name', 'position', 'position__name')

    print(list(
        subordinates))  # TODO: remove console log

    return JsonResponse({'subordinates': list(subordinates)})


class EmployeeListView(LoginRequiredMixin,
                       generic.ListView):
    model = Employee
    context_object_name = "employee_list"
    template_name = "staff_management/employee/employee_list.html"
    paginate_by = 10
