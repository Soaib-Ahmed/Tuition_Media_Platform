from django.db import models
from django.contrib.auth.models import User


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

class Tuition(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    subjects = models.CharField(max_length=1000, null=False, verbose_name='Subjects')
    type = models.CharField(max_length=200, null=False, verbose_name='Type')
    grade = models.CharField(max_length=200, null=False, verbose_name='Class', choices=CLASS_CHOICES)
    gender = models.CharField(max_length=10, choices=GENDER_TYPE)
    pref_gender = models.CharField(max_length=20, choices=GENDER_TYPE, verbose_name='Preferred Gender')
    student_count = models.IntegerField(verbose_name='Student Count')
    teaching_time = models.CharField(max_length=200, verbose_name='Teaching Time')
    days_per_week = models.IntegerField(null=False, verbose_name='How many days a week')
    location = models.CharField(max_length=1000, null=False, verbose_name='Location')
    monthly_salary = models.IntegerField(null=False, verbose_name='Monthly Salary')
    availability = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class TuitionApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tuition = models.ForeignKey(Tuition, on_delete=models.CASCADE)
    applied_date = models.DateTimeField(auto_now_add=True)
    is_chosen = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.tuition.title}"

class TuitionApplicationAdmin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tuition = models.ForeignKey(Tuition, on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.tuition.title}"

class TuitionReview(models.Model):
    tuition = models.ForeignKey('Tuition', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review_text = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.tuition.title}"