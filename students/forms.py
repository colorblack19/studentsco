from django import forms
from .models import Student
from .models import FeeStructure
from django.contrib.auth.models import User

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'first_name', 'last_name', 'gender', 'age',
            'parent_name', 'phone_number', 'parent_id_number',
            'class_level', 'teacher',   # ✅ ADD THIS
            'status', 'feestructure', 'photo', 'balance'
        ]

        widgets = {
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'class_level': forms.Select(attrs={'class': 'form-select'}),
            'teacher': forms.Select(attrs={'class': 'form-select'}),  # ✅
            'feestructure': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ✅ SHOW ONLY TEACHERS
        self.fields['teacher'].queryset = User.objects.filter(groups__name="Teacher")
        self.fields['teacher'].label = "Assign Teacher"


class FeeStructureForm(forms.ModelForm):
    class Meta:
        model = FeeStructure
        fields = ['class_name', 'amount']
