from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime
from typing import Optional, Union
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Count
from django.urls import reverse


class Employee(AbstractUser):
    full_name: Optional[str] = models.CharField(max_length=128, null=True)
    position: Optional["Position"] = models.ForeignKey(
        "Position",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="employees",
    )
    hired: Optional[datetime] = models.DateField(null=True, blank=True)
    email: str = models.EmailField(unique=True)
    supervisor: Optional["self"] = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="subordinates",
    )
    is_staff: bool = models.BooleanField(default=False)
    is_superuser: bool = models.BooleanField(default=False)
    username: Optional[str] = models.CharField(
        max_length=128, unique=True, blank=True, null=True
    )
    first_name: Optional[str] = models.CharField(
        max_length=128,
        blank=True,
        null=True
    )
    last_name: Optional[str] = models.CharField(
        max_length=128,
        blank=True,
        null=True
    )

    class Meta:
        unique_together = ("full_name", "email")

    def __str__(self) -> str:
        return self.full_name if self.full_name else "Unnamed Employee"

    def clean(self) -> None:
        if not self.full_name:
            self.full_name = f"{self.first_name} {self.last_name}"

        if self.email and not self.email_validator(self.email):
            raise ValidationError("Invalid email format")

        if self.supervisor and self.supervisor == self:
            raise ValidationError("Employee cannot be their own supervisor")

        if not self.hired:
            self.hired = datetime.now()

    def save(self, *args: Union[str, None],
             **kwargs: Union[str, None]) -> None:
        is_update = self.pk is not None
        if is_update:
            old_instance = Employee.objects.get(pk=self.pk)
            if old_instance.position != self.position:
                self.handle_hierarchy_change(old_instance)
        self.username = self.email
        super().save(*args, **kwargs)
        print(f"Employee {self.full_name} saved.")

    def delete(self, *args: Union[str, None],
               **kwargs: Union[str, None]) -> None:
        if self.subordinates.exists():
            print(
                f"Employee {self.full_name} has subordinates."
                f" Reassigning them."
            )
            self.reassign_subordinates(self.position.hierarchy_level)
        super(Employee, self).delete(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse("staff_management:employee-detail",
                       kwargs={"pk": self.pk})

    def handle_hierarchy_change(self, old_instance: "Employee") -> None:
        try:
            old_position_level = old_instance.position.hierarchy_level
            new_position_level = self.position.hierarchy_level
        except Exception as er:
            print(er)
            return

        self.reassign_subordinates(old_position_level)

        new_supervisor = self._find_supervisor_by_hierarchy(
            new_position_level + 1, self.pk
        )
        if new_supervisor:
            self.supervisor = new_supervisor
            print(
                f"{self.full_name}'s new supervisor:"
                f" {self.supervisor.full_name}"
            )

    def reassign_subordinates(self, old_position_level: int) -> None:
        new_supervisor = self._find_supervisor_by_hierarchy(old_position_level,
                                                            self.pk)
        if new_supervisor:
            self.subordinates.update(supervisor=new_supervisor)
            print(
                f"Subordinates of {self.full_name} "
                f"reassigned to new supervisor: {new_supervisor.full_name}"
            )
        else:
            self.subordinates.update(supervisor=None)
            print(
                f"No suitable supervisor found for subordinates "
                f"of {self.full_name}. Subordinates set to None."
            )

        for subordinate in self.subordinates.all():
            subordinate.reassign_subordinates(old_position_level)

    @staticmethod
    def _find_supervisor_by_hierarchy(
            hierarchy_level: int, id_to_exclude: Optional[int] = None
    ) -> Optional["Employee"]:
        print(hierarchy_level, id_to_exclude)

        supervisors = Employee.objects.filter(
            position__hierarchy_level=hierarchy_level)

        if id_to_exclude is not None:
            supervisors = supervisors.exclude(id=id_to_exclude)

        return (
            supervisors.annotate(num_subordinates=Count("subordinates"))
            .order_by("num_subordinates")
            .first()
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


class Position(models.Model):
    LVL_1_POSITION_CHOICES = [("position_1", "Start position")]
    LVL_2_POSITION_CHOICES = [("manager", "Manager")]
    LVL_3_POSITION_CHOICES = [("department_head", "Department Head")]
    LVL_4_POSITION_CHOICES = [("coo", "Chief Operating Officer (COO)")]
    LVL_5_POSITION_CHOICES = [("cfo", "Chief Financial Officer (CFO)")]
    LVL_6_POSITION_CHOICES = [("ceo", "Chief Executive Officer (CEO)")]
    LVL_7_POSITION_CHOICES = [("chairman", "Chairman")]

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
        null=True, validators=[MinValueValidator(1), MaxValueValidator(7)]
    )

    class Meta:
        unique_together = ("name", "hierarchy_level")

    def __str__(self):
        return self.name

    def clean(self) -> None:
        if self.name not in dict(self.POSITION_CHOICES[self.hierarchy_level]):
            raise ValidationError(
                f"Invalid position name for level {self.hierarchy_level}."
            )
