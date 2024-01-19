from django.contrib import admin
from .models import Tuition, TuitionApplication, TuitionReview

admin.site.register(Tuition)
admin.site.register(TuitionApplication)
admin.site.register(TuitionReview)