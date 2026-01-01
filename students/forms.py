from django import forms
from .models import Student
from .models import FeeStructure
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
from .models import AcademicReport, ReportSubject, Subject

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
        fields = [
            'class_name',
            'amount',
            'opening_amount',
            'deadline',
            'notes'
        ]

        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }





class AcademicReportForm(forms.ModelForm):
    class Meta:
        model = AcademicReport
        fields = [
            "term",
            "total_score",
            "grade",
            "teacher_comment",
            "headteacher_remark",
            "status",
        ]
        widgets = {
            "teacher_comment": forms.Textarea(attrs={"rows": 3}),
            "headteacher_remark": forms.Textarea(attrs={"rows": 3}),
        }


class ReportSubjectForm(forms.ModelForm):
    class Meta:
        model = ReportSubject
        fields = ["subject", "marks", "grade", "teacher_comment"]

    def __init__(self, *args, **kwargs):
        student = kwargs.pop("student", None)
        super().__init__(*args, **kwargs)

        if student:
            self.fields["subject"].queryset = Subject.objects.filter(
                class_level=student.class_level
            )


ReportSubjectFormSet = inlineformset_factory(
    AcademicReport,
    ReportSubject,
    form=ReportSubjectForm,
    extra=1,
    can_delete=True 
)
