from django import forms
from .models import Student
from .models import FeeStructure

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'first_name', 'last_name', 'gender', 'age', 'parent_name',
            'phone_number', 'parent_id_number', 'class_level',
            'status', 'feestructure', 'photo', 'balance'
        ]

        widgets = {
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'class_level': forms.Select(attrs={'class': 'form-select'}),
            'feestructure': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class FeeStructureForm(forms.ModelForm):
    class Meta:
        model = FeeStructure
        fields = ['class_name', 'amount']