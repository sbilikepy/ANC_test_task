from django.db.models import Q
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from .forms import EmployeeSearchForm, EmployeeForm
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from .models import Employee


def index(request: HttpRequest) -> HttpResponse:
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
        levels = range(1, 8)
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

    return JsonResponse({'subordinates': list(subordinates)})


class EmployeeListView(generic.ListView):
    model = Employee
    context_object_name = "employee_list"
    template_name = "staff_management/employee/employee_list.html"
    paginate_by = 5

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["search_form"] = EmployeeSearchForm(self.request.GET)
        context["sort"] = self.request.GET.get("sort",
                                               "position__hierarchy_level")
        context["direction"] = self.request.GET.get("direction", "asc")
        return context


@csrf_exempt
def load_employees_for_list_view(request: HttpRequest) -> JsonResponse:
    print("CALL")
    sort = request.GET.get("sort", "position__hierarchy_level")
    direction = request.GET.get("direction", "asc")

    if direction == "desc":
        sort = f"-{sort}"

    search_query = request.GET.get("search", "")
    queryset = Employee.objects.all()
    print(search_query)
    print()
    if search_query:
        queryset = queryset.filter(
            Q(full_name__icontains=search_query)
            | Q(first_name__icontains=search_query)
            | Q(last_name__icontains=search_query)
            | Q(email__icontains=search_query)
            | Q(position__name__icontains=search_query)
            | Q(hired__icontains=search_query)
            | Q(hired__icontains=search_query.replace(".", "-"))
            | Q(hired__icontains=search_query.replace("/", "-"))
        )

    queryset = queryset.order_by(sort)

    employees = list(
        queryset.values("id", "full_name", "position__name", "hired", "email")
    )

    data = {"employees": employees}

    return JsonResponse(data)


class EmployeeCreateView(LoginRequiredMixin, generic.CreateView):
    model = Employee
    template_name = "staff_management/employee/employee_form.html"
    form_class = EmployeeForm

    def get_success_url(self) -> str:
        return reverse(
            "staff_management:employee-detail",
            kwargs={"pk": self.object.pk}
        )


class EmployeeDetailView(LoginRequiredMixin, generic.DetailView):
    model = Employee
    template_name = "staff_management/employee/employee_detail.html"


class EmployeeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Employee
    template_name = "staff_management/employee/employee_form.html"
    form_class = EmployeeForm


class EmployeeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Employee
    template_name = "staff_management/employee/employee_confirm_delete.html"
    success_url = reverse_lazy("staff_management:employee-list")


def crud_info(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        template_name="staff_management/employee/crud_info.html"
    )
