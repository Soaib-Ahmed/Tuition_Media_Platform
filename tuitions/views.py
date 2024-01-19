from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from .models import Tuition, TuitionApplication, TuitionReview
from .forms import TuitionApplicationForm, TuitionReviewForm
from django.contrib import messages
from django.http import HttpResponseRedirect

class TuitionListView(ListView):
    model = Tuition
    template_name = 'tuitions/tuition_list.html'
    context_object_name = 'tuitions'

class TuitionDetailView(DetailView):
    model = Tuition
    template_name = 'tuitions/tuition_detail.html'
    context_object_name = 'tuition'
    form_class = TuitionApplicationForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['tuition'] = self.get_object()
        return kwargs

    def post(self, request, *args, **kwargs):
        tuition = self.get_object()

        application_form = TuitionApplicationForm(data=request.POST, user=request.user, tuition=tuition)
        if application_form.is_valid():
            if TuitionApplication.objects.filter(user=request.user, tuition=tuition).exists():
                messages.warning(request, "You have already applied for this tuition.")
                return HttpResponseRedirect(request.path)

            application = application_form.save(commit=False)
            application.user = request.user
            application.tuition = tuition
            application.save()

            messages.success(request, "Application submitted successfully.")
            return HttpResponseRedirect(request.path)
        else:
            messages.error(request, "Error submitting application. Please check the form.")


        if 'leave_review' in request.POST:
            review_form = TuitionReviewForm(request.POST)
            if review_form.is_valid() and self.user_has_accepted_tuition(request.user, tuition):
                review = review_form.save(commit=False)
                review.user = request.user
                review.tuition = tuition
                review.save()

                messages.success(request, 'Your review has been submitted successfully.')

                return redirect('tuitions:tuition-detail', pk=tuition.id)

        return self.get(request, *args, **kwargs)

    @staticmethod
    def user_has_accepted_tuition(user, tuition):
        try:
            application = TuitionApplication.objects.get(user=user, tuition=tuition)
            return application.is_accepted
        except TuitionApplication.DoesNotExist:
            return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tuition = self.object
        reviews = tuition.reviews.all()
        review_form = TuitionReviewForm()
        application_form = TuitionApplicationForm(user=self.request.user, tuition=tuition)

        user_has_applied = (
            self.request.user.is_authenticated and
            TuitionApplication.objects.filter(user=self.request.user, tuition=tuition).exists()
        )

        user_has_accepted_tuition = (
            user_has_applied and
            TuitionApplication.objects.get(user=self.request.user, tuition=tuition).is_accepted
        )

        context['reviews'] = reviews
        context['review_form'] = review_form
        context['application_form'] = application_form
        context['user_has_applied'] = user_has_applied
        context['user_has_accepted_tuition'] = user_has_accepted_tuition
        return context