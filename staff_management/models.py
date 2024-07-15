from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Count
from django.urls import reverse


class Employee(AbstractUser):
    full_name = models.CharField(max_length=128, null=True)
    position = models.ForeignKey(
        "Position",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="employees",
    )

    hired = models.DateField(
        null=True,
        blank=True,
    )
    email = models.EmailField(unique=True)

    supervisor = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="subordinates",
    )
    is_staff = models.BooleanField(
        default=False
    )
    is_superuser = models.BooleanField(
        default=False
    )
    username = models.CharField(
        max_length=128, unique=True, blank=True,
        null=True
    )
    first_name = models.CharField(
        max_length=128, unique=False, blank=True,
        null=True
    )
    last_name = models.CharField(
        max_length=128, unique=False, blank=True,
        null=True
    )

    def __str__(self):
        return self.full_name if self.full_name else "Unnamed Employee"

    def get_absolute_url(self):
        return reverse("staff_management:employee-detail",
                       kwargs={"pk": self.pk})

    def clean(self) -> None:
        print("CLEAN CALL")
        if not self.full_name:
            self.full_name = f"{self.first_name} {self.last_name}"

        if self.email and not self.email_validator(self.email):
            raise ValidationError("Invalid email format")

        if self.supervisor and self.supervisor == self:
            raise ValidationError("Employee cannot be their own supervisor")

        if not self.hired:
            self.hired = datetime.now()

    def save(self, *args, **kwargs) -> None:
        if self.pk:
            try:
                old_instance = Employee.objects.get(pk=self.pk)
            except Employee.DoesNotExist:
                pass
            else:
                if (
                        old_instance.position.hierarchy_level
                        != self.position.hierarchy_level
                ):
                    print(
                        f"Hierarchy level changed for {self.full_name}. "
                        f"Reassigning subordinates."
                    )
                    self.reassign_subordinates("update")
                    new_supervisor = (
                        Employee.objects.filter(
                            position__hierarchy_level=self.position.hierarchy_level + 1
                        )
                        .annotate(num_subordinates=Count("subordinates"))
                        .order_by("num_subordinates")
                        .first()
                    )
                    self.supervisor = new_supervisor

        self.username = self.email
        super(Employee, self).save(*args, **kwargs)
        print(f"Employee {self.full_name} saved.")

    def delete(self, *args, **kwargs):
        if self.subordinates.exists():
            print(
                f"Employee {self.full_name} has subordinates."
                f" Reassigning them.")
            self.reassign_subordinates("delete")
        super(Employee, self).delete(*args, **kwargs)

    def reassign_subordinates(self, event_type: str) -> None:

        if event_type == "update":
            next_hierarchy_level = self.position.hierarchy_level
        else:
            next_hierarchy_level = self.position.hierarchy_level + 1

        new_supervisor = (
            Employee.objects.filter(
                position__hierarchy_level=next_hierarchy_level - 1)
            .annotate(num_subordinates=Count("subordinates"))
            .order_by("num_subordinates")
            .first()
        )

        if new_supervisor:
            self.subordinates.update(supervisor=new_supervisor)
            print(
                f"Subordinates of {self.full_name} "
                f"reassigned to new supervisor: {new_supervisor.full_name}"
            )
        else:
            self.subordinates.update(supervisor=None)
            print(
                f"No suitable supervisor found for {self.full_name}."
                f" Subordinates set to None."
            )

    @staticmethod
    def email_validator(email: str) -> bool:
        from django.core.validators import validate_email
        from django.core.exceptions import ValidationError

        try:
            validate_email(email)
            return True
        except ValidationError:
            return False

    class Meta:
        unique_together = ("full_name", "email")


class Position(models.Model):
    LVL_1_POSITION_CHOICES = [
        ("position_1", "Start position"),
    ]

    LVL_2_POSITION_CHOICES = [
        ("manager", "Manager"),
    ]

    LVL_3_POSITION_CHOICES = [
        ("department_head", "Department Head"),
    ]

    LVL_4_POSITION_CHOICES = [
        ("coo", "Chief Operating Officer (COO)"),
    ]

    LVL_5_POSITION_CHOICES = [
        ("cfo", "Chief Financial Officer (CFO)"),
    ]

    LVL_6_POSITION_CHOICES = [
        ("ceo", "Chief Executive Officer (CEO)"),
    ]

    LVL_7_POSITION_CHOICES = [
        ("chairman", "Chairman"),
    ]

    POSITION_CHOICES = {
        1: LVL_1_POSITION_CHOICES,
        2: LVL_2_POSITION_CHOICES,
        3: LVL_3_POSITION_CHOICES,
        4: LVL_4_POSITION_CHOICES,
        5: LVL_5_POSITION_CHOICES,
        6: LVL_6_POSITION_CHOICES,
        7: LVL_7_POSITION_CHOICES,
    }

    ALL_POSITION_CHOICES = sum(POSITION_CHOICES.values(), [])

    name = models.CharField(
        max_length=128,
        choices=ALL_POSITION_CHOICES,
        unique=True
    )
    hierarchy_level = models.IntegerField(
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(7)]
    )

    def clean(self):
        if self.name not in dict(self.POSITION_CHOICES[self.hierarchy_level]):
            raise ValidationError(
                f"Invalid position name for level {self.hierarchy_level}."
            )

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ("name", "hierarchy_level")
