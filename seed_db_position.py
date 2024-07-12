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

    lvl_6_count = 0
    lvl_5_count = 0
    lvl_4_count = 0
    lvl_3_count = 0
    lvl_2_count = 0
    lvl_1_count = 0

    for employee_without_position in Employee.objects.filter(position=None):
        if lvl_6_count < 10:
            employee_without_position.position = Position.objects.get(pk=6)
            employee_without_position.save()
            lvl_6_count += 1

        if lvl_5_count < 50:
            employee_without_position.position = Position.objects.get(pk=5)
            employee_without_position.save()
            lvl_5_count += 1

        if lvl_4_count < 250:
            employee_without_position.position = Position.objects.get(pk=4)
            employee_without_position.save()
            lvl_4_count += 1

        if lvl_3_count < 500:
            employee_without_position.position = Position.objects.get(pk=3)
            employee_without_position.save()
            lvl_3_count += 1

        elif lvl_2_count < 2000:
            employee_without_position.position = Position.objects.get(pk=2)
            employee_without_position.save()
            lvl_2_count += 1

        else:
            employee_without_position.position = Position.objects.get(pk=1)
            employee_without_position.save()
            lvl_1_count += 1

    # for i in Employee.objects.all():
    #     i.position_id = None
    #     i.save()
    print("Positions sorted")


if __name__ == "__main__":
    assign_positions()
