# from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth import login
from .forms import SignupForm
from django.views.generic.edit import FormView
from django.http import HttpResponse
from .tasks import sendEmail

# Create your views here.


def send_email(request):
    sendEmail.delay()
    return HttpResponse("<h1>Done Sending</h1>")


class SignupView(FormView):
    template_name = "registration/signup.html"
    form_class = SignupForm
    success_url = reverse_lazy("todo:task_list")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
