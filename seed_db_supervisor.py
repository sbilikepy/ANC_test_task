import os
import random
from typing import List

import django
from django.db.models import Count

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "EmployeeManagementDjangoProject.settings"
)
django.setup()

from staff_management.models import Employee, Position


def assign_supervisors() -> None:
    for level in range(6, 0, -1):

        print(f"Assigning supervisors for level {level}")
        employees_to_process = Employee.objects.filter(supervisor=None)
        employees = employees_to_process.filter(
            position__hierarchy_level=level)
        higher_level_employees = Employee.objects.filter(
            position__hierarchy_level=level + 1
        )

        if not higher_level_employees.exists():
            print(f"No supervisors found for level {level}")
            continue

        for employee in employees:
            supervisor = random.choice(higher_level_employees)
            employee.supervisor = supervisor
            employee.save()
            print(
                f"New relation: {employee.full_name} "
                f"(lvl {employee.position.hierarchy_level}):"
                f" {supervisor.full_name} "
                f"(lvl {supervisor.position.hierarchy_level})"
            )

    print("Relations created")
    unassigned: bool = True
    while unassigned:
        for level in range(7, 1, -1):
            unassigned_counter = 0
            supervisors_without_subordinates = Employee.objects.annotate(
                num_subordinates=Count("subordinates")
            ).filter(position__hierarchy_level=level, num_subordinates=0)
            print(
                f"Level {level} | {supervisors_without_subordinates.count()} "
                f"are "
                f"being processed")
            unassigned_counter += len(supervisors_without_subordinates)

            lower_level_employees = (
                Employee.objects.filter(position__hierarchy_level=level - 1)
                .annotate(
                    supervisor_subordinate_count=Count(
                        "supervisor__subordinates")
                )
                .filter(supervisor_subordinate_count__gt=1)
            )

            if not lower_level_employees.exists():
                print(f"No subordinates found for level {level}")
                continue

            for supervisor in supervisors_without_subordinates:
                subordinate = random.choice(lower_level_employees)
                subordinate.supervisor = supervisor
                subordinate.save()
                print(
                    f"New relation: {supervisor.full_name} "
                    f"(lvl {supervisor.position.hierarchy_level}):"
                    f" {subordinate.full_name} "
                    f"(lvl {subordinate.position.hierarchy_level})"
                )
            unassigned_counter += len(supervisors_without_subordinates)
            if unassigned_counter == 0:
                unassigned = False
        print("Subordinates assigned")
    errors: List[Employee] = []
    for employee in Employee.objects.all():
        try:
            employee.supervisor
        except Exception as er:
            print(er)
            errors.append(employee)
    for problem_emp in errors:
        hierarchy_lvl = problem_emp.position.hierarchy_level
        hierarchy_lvl += 1
        new_supervisor = Employee.objects.filter(
            position__hierarchy_level=hierarchy_lvl
        ).first()
        problem_emp.supervisor = new_supervisor
        print(problem_emp, "fixed")
        problem_emp.save()


def control_check():
    all_employees = Employee.objects.filter(position__hierarchy_level__lt=7)
    for employee in all_employees:
        print(employee)
        correct_level = employee.position.hierarchy_level + 1
        actual_level = employee.supervisor.position.hierarchy_level
        if actual_level != correct_level:
            print("actual_level != correct_level")
            print(employee, correct_level, actual_level)
            new_chief = Employee.objects.filter(
                position__hierarchy_level=correct_level
            ).first()
            try:
                employee.supervisor = new_chief
                employee.save()
            except Exception as er:
                print(er, employee, correct_level, actual_level)
    print("Control check passed!")


if __name__ == "__main__":
    assign_supervisors()
    control_check()
