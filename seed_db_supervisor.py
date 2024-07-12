import os
import random
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "EmployeeManagementDjangoProject.settings")
django.setup()

from staff_management.models import Employee, Position


def assign_supervisors():
    for level in range(3, 0, -1):
        print(level)
        employees = Employee.objects.filter(position__hierarchy_level=level)
        higher_level_employees = Employee.objects.filter(
            position__hierarchy_level=level + 1)

        for employee in employees:
            supervisor = random.choice(higher_level_employees)
            employee.supervisor = supervisor
            employee.save()
            print(f"New relation: {employee.full_name} ("
                  f"lvl {employee.position.hierarchy_level}):"
                  f" {supervisor.full_name} (lvl "
                  f"{supervisor.position.hierarchy_level})")


if __name__ == "__main__":
    assign_supervisors()
