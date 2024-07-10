from django.db import models


class Employee(AbstractUser):
    full_name = models.CharField(max_length=128, null=True)

    position = models.ForeignKey("Position",
                                 on_delete=models.CASCADE,
                                 null=True,  # TODO: set to False after db fill
                                 related_name="employees")

    hired = models.DateField()
    email = models.EmailField(unique=True)

    supervisor = models.ForeignKey("self",
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   # TODO: set to False after db fill
                                   related_name="subordinates")

    def __str__(self):
        return f"{self.full_name}. Position: {self.position}"

    def clean(self):
        if not self.full_name:
            self.full_name = f"{self.first_name} {self.last_name}"

        if self.email and not self.email_validator(self.email):
            raise ValidationError("Invalid email format")

        if self.supervisor and self.supervisor == self:
            raise ValidationError("Employee cannot be their own supervisor")

    @staticmethod
    def email_validator(email):
        from django.core.validators import validate_email
        from django.core.exceptions import ValidationError

        try:
            validate_email(email)
            return True
        except ValidationError:
            return False

    class Meta:
        pass


class Position(models.Model):
    LVL_1_POSITION_CHOICES = [
        ('position_1', 'Position 1'),
        ('position_2', 'Position 2'),
        ('position_3', 'Position 3'),
        ('position_4', 'Position 4'),
    ]

    LVL_2_POSITION_CHOICES = [
        ('manager', 'Manager'),
    ]

    LVL_3_POSITION_CHOICES = [
        ('department_head', 'Department Head'),
    ]

    LVL_4_POSITION_CHOICES = [
        ('coo', 'Chief Operating Officer (COO)'),
    ]

    LVL_5_POSITION_CHOICES = [
        ('cfo', 'Chief Financial Officer (CFO)'),
    ]

    LVL_6_POSITION_CHOICES = [
        ('ceo', 'Chief Executive Officer (CEO)'),
    ]

    LVL_7_POSITION_CHOICES = [
        ('chairman', 'Chairman'),
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
        choices=ALL_POSITION_CHOICES
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
        unique_together = ('name', 'hierarchy_level')
