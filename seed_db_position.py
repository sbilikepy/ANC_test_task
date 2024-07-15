import os

import django
from django.db import transaction

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "EmployeeManagementDjangoProject.settings"
)
django.setup()

from staff_management.models import Employee, Position


@transaction.atomic
def assign_positions() -> None:
    position_counts = {7: 1,
                       6: 10,
                       5: 50,
                       4: 250,
                       3: 1250,
                       2: 6250,
                       1: None}

    employees_without_position = Employee.objects.filter(
        position=None).order_by("id")

    for employee in employees_without_position:
        for position, count in position_counts.items():
            if count is None or count > 0:
                employee.position = Position.objects.get(pk=position)
                employee.save()
                if count is not None:
                    position_counts[position] -= 1
                break

    print("Positions assigned")


if __name__ == "__main__":
    assign_positions()
