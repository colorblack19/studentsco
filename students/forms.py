

from django import forms
from .models import Student
from .models import FeeStructure
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
from .models import AcademicReport, ReportSubject, Subject




class StudentForm(forms.ModelForm):

    # ✅ EXTRA MANY TEACHERS
    extra_teachers = forms.ModelMultipleChoiceField(
    queryset=User.objects.filter(groups__name="Teacher"),
    widget=forms.CheckboxSelectMultiple(
        attrs={'class': 'form-check'}
    ),
    required=False
)


    class Meta:
        model = Student
        fields = [
            'first_name', 'last_name', 'gender', 'age',
            'parent_name', 'phone_number', 'parent_id_number',
            'class_level',
            'teacher',          # MAIN TEACHER (unchanged)
            'extra_teachers',   # ✅ MANY TEACHERS
            'status', 'feestructure', 'photo', 'balance'
        ]

        widgets = {
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'class_level': forms.Select(attrs={'class': 'form-select'}),
            'teacher': forms.Select(attrs={'class': 'form-select'}),
            'feestructure': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ✅ SHOW ONLY TEACHERS
        self.fields['teacher'].queryset = User.objects.filter(groups__name="Teacher")
        self.fields['teacher'].label = "Main Teacher"

class StudentTeacherForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ["teacher", "extra_teachers"]

        widgets = {
            "teacher": forms.Select(attrs={"class": "form-select"}),
            "extra_teachers": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # show only teachers
        self.fields['teacher'].queryset = User.objects.filter(groups__name="Teacher")

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
            "teacher_comment",
            "headteacher_remark",
            "status",
        ]
        widgets = {
            "teacher_comment": forms.Textarea(attrs={"rows": 3}),
            "headteacher_remark": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk and self.instance.status == "PUBLISHED":
            for field in self.fields.values():
                field.disabled = True

class ReportSubjectForm(forms.ModelForm):
    class Meta:
        model = ReportSubject
        fields = ["subject", "marks", "grade", "teacher_comment"]
        widgets = {
            "grade": forms.TextInput(attrs={
                "readonly": "readonly",
                "class": "form-control bg-light"
            })
        }

    def __init__(self, *args, **kwargs):
        student = kwargs.pop("student", None)
        super().__init__(*args, **kwargs)

        if student:
            self.fields["subject"].queryset = Subject.objects.all()


ReportSubjectFormSet = inlineformset_factory(
    AcademicReport,
    ReportSubject,
    form=ReportSubjectForm,
    extra=1,
    can_delete=True 
)
