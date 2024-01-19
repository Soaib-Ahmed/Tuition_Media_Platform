from django.views.generic import TemplateView
from tuitions.models import Tuition
from tuitions.forms import TuitionFilterForm

class HomePageView(TemplateView):
    template_name = 'home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        tuitions = Tuition.objects.all()
        filter_form = TuitionFilterForm(self.request.GET)

        if filter_form.is_valid():
            tuitions = filter_form.filter_tuitions(tuitions)

        context['tuitions'] = tuitions
        context['filter_form'] = filter_form


        return context