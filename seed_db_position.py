import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "EmployeeManagementDjangoProject.settings")
django.setup()

from staff_management.models import Employee, Position


def assign_positions():
    for position_id in range(4, 8)[::-1]:
        if len(Employee.objects.filter(
                position__hierarchy_level=position_id)) == 0:
            candidate = Employee.objects.filter(position=None).first()
            new_position = Position.objects.get(pk=position_id)
            candidate.position = new_position
            if position_id != 7:
                candidate.supervisor = Employee.objects.filter(
                    position__hierarchy_level__exact=position_id + 1).first()
            candidate.save()
    positions_counter = 0
    for employee_without_position in Employee.objects.filter(position=None):
        if positions_counter < 200:
            employee_without_position.position = Position.objects.get(pk=3)
            employee_without_position.save()
            positions_counter += 1

        elif positions_counter < 300:
            employee_without_position.position = Position.objects.get(pk=2)
            employee_without_position.save()
            positions_counter += 1

        else:
            employee_without_position.position = Position.objects.get(pk=1)
            employee_without_position.save()

    # for i in Employee.objects.all():
    #     i.position_id = None
    #     i.save()
    print("Positions sorted")


if __name__ == "__main__":
    assign_positions()
