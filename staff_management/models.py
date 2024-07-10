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

