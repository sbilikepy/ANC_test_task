import os

import django
from django.db.models import Count

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "EmployeeManagementDjangoProject.settings"
)
django.setup()

from staff_management.models import Employee, Position


def assign_positions() -> None:
    position_counts = {7: 2,
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
            if Employee.objects.filter(
                    position__hierarchy_level=position).count() == count:
                print(f"Level {position}: employee amount capped")
                break

            if count is None or count > 0:
                employee.position = Position.objects.get(pk=position)
                employee.save()
                if count is not None:
                    position_counts[position] -= 1
                break

    print("Positions assigned")


def fix_positions() -> None:
    for employee in Employee.objects.all():
        position = employee.position
        supervisor = employee.supervisor

        if position is None:
            continue

        if position.hierarchy_level == 7:

            if supervisor is not None:
                employee.supervisor = None
                employee.save()
                print(
                    f"Removed supervisor from employee {employee.full_name}.")
        else:

            if supervisor is not None and supervisor.position.hierarchy_level != position.hierarchy_level + 1:

                new_supervisor = (
                    Employee.objects.filter(
                        position__hierarchy_level=position.hierarchy_level + 1)
                    .annotate(num_subordinates=Count("subordinates"))
                    .order_by("num_subordinates")
                    .first()
                )

                if new_supervisor:
                    employee.supervisor = new_supervisor
                    employee.save()
                    print(
                        f"Reassigned supervisor for "
                        f"employee {employee.full_name} "
                        f"to {new_supervisor.full_name}.")
                else:
                    print(
                        f"No suitable new supervisor "
                        f"found for employee {employee.full_name}.")
            elif supervisor is None:

                new_supervisor = (
                    Employee.objects.filter(
                        position__hierarchy_level=position.hierarchy_level + 1)
                    .annotate(num_subordinates=Count("subordinates"))
                    .order_by("num_subordinates")
                    .first()
                )

                if new_supervisor:
                    employee.supervisor = new_supervisor
                    employee.save()
                    print(
                        f"Assigned supervisor for employee {employee.full_name} to {new_supervisor.full_name}.")
                else:
                    print(
                        f"No suitable supervisor found for employee {employee.full_name}.")

    print("Positions fixed")


if __name__ == "__main__":
    assign_positions()
    fix_positions()
