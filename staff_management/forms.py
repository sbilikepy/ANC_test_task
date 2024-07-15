from django import forms
from .models import Employee, Position


class EmployeeSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search for an employee"}),
    )


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ["full_name", "position", "hired", "email", "supervisor"]
        widgets = {
            "full_name": forms.TextInput(
                attrs={"class": "form-control",
                       "placeholder": "Enter full name"}
            ),
            "position": forms.Select(
                attrs={"class": "form-control",
                       "placeholder": "Select position"}
            ),
            "hired": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                    "placeholder": "Select hiring date",
                }
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control",
                       "placeholder": "example@somemail.com"}
            ),
            "supervisor": forms.Select(
                attrs={"class": "form-control",
                       "placeholder": "Select supervisor"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["position"].queryset = Position.objects.all()
        self.fields["supervisor"].queryset = Employee.objects.order_by(
            "full_name")
