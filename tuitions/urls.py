from django.urls import path
from .views import TuitionListView, TuitionDetailView

app_name = 'tuitions'

urlpatterns = [
    path('tuitions/', TuitionListView.as_view(), name='tuition-list'),
    path('tuitions/<int:pk>/', TuitionDetailView.as_view(), name='tuition-detail'),
]