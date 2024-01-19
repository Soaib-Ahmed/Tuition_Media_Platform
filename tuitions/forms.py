from django import forms
from .models import TuitionApplication, TuitionApplicationAdmin,TuitionReview
GENDER_TYPE = (
    ('Male', 'Male'),
    ('Female', 'Female'),
)

CLASS_CHOICES = [
    ('Class 1', 'Class 1'),
    ('Class 2', 'Class 2'),
    ('Class 3', 'Class 3'),
    ('Class 4', 'Class 4'),
    ('Class 5', 'Class 5'),
    ('Class 6', 'Class 6'),
    ('Class 7', 'Class 7'),
    ('Class 8', 'Class 8'),
    ('Class 9', 'Class 9'),
    ('Class 10', 'Class 10'),
    ('Class 11', 'Class 11'),
    ('Class 12', 'Class 12'),
    ('Admission Test', 'Admission Test'),
    ('IELTS', 'IELTS'),
    ('BCS & Job Test', 'BCS & Job Test'),
]

class TuitionFilterForm(forms.Form):
    grade = forms.ChoiceField(choices=CLASS_CHOICES, required=False, label='Class')

    def filter_tuitions(self, tuitions):
        if self.cleaned_data['grade']:
            tuitions = tuitions.filter(grade=self.cleaned_data['grade'])
        return tuitions

class TuitionApplicationForm(forms.ModelForm):
    class Meta:
        model = TuitionApplication
        fields = ['tuition']

    def __init__(self, *args, user=None, tuition=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.tuition = tuition


class TuitionApplicationAdminForm(forms.ModelForm):
    class Meta:
        model = TuitionApplicationAdmin
        fields = ['is_accepted']

class TuitionReviewForm(forms.ModelForm):
    class Meta:
        model = TuitionReview
        fields = ['review_text']

class TuitionAdminChooseForm(forms.Form):
    applicant_id = forms.IntegerField()

    def clean_applicant_id(self):
        applicant_id = self.cleaned_data['applicant_id']
        if not TuitionApplication.objects.filter(id=applicant_id).exists():
            raise forms.ValidationError('Invalid applicant ID.')
        return applicant_id
