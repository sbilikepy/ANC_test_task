import os

import django
from django_seed import Seed

os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "EmployeeManagementDjangoProject.settings")
django.setup()

from staff_management.models import Employee, Position


def seed_users(amount):
    seeder = Seed.seeder()

    seeder.add_entity(Employee, amount, {
        'email': lambda x: unique_email(seeder),
        'full_name': lambda
            x: f"{seeder.faker.first_name()} {seeder.faker.last_name()}",
        'hired': lambda x: seeder.faker.date_this_decade(before_today=True,
                                                         after_today=False),
        'username': lambda x: unique_username(seeder),
        'first_name': '',
        'last_name': '',
        'is_superuser': 0,
        'is_staff': 0,
        'is_active': 0,
        'supervisor_id': ''
    })

    inserted_pks = seeder.execute()

    for pk in inserted_pks[Employee]:
        user = Employee.objects.get(pk=pk)
        user.set_password(f'seed_password{pk}')
        user.save()
    print(f"{amount} users has been created.")


def unique_email(seeder):
    email = seeder.faker.email()
    while Employee.objects.filter(email=email).exists():
        email = seeder.faker.email()
    return email


def unique_username(seeder):
    username = seeder.faker.user_name()
    while Employee.objects.filter(username=username).exists():
        username = seeder.faker.user_name()
    return username


if __name__ == "__main__":
    seed_users(50_000)
