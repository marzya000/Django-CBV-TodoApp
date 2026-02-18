# from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth import login
from .forms import SignupForm
from django.views.generic.edit import FormView

# Create your views here.


class SignupView(FormView):
    template_name = "registration/signup.html"
    form_class = SignupForm
    success_url = reverse_lazy("todo:task_list")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
