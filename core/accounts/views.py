# from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth import login
from .forms import SignupForm
from django.views.generic.edit import FormView
from django.http import HttpResponse
import time
import requests
from .tasks import sendEmail
from django.http import HttpResponse,JsonResponse
from django.views.decorators.cache import cache_page

# Create your views here.


def send_email(request):
    sendEmail.delay()
    return HttpResponse('<h1>Done Sending</h1>')


@cache_page(60*20)
def weather_view(request,city):  
    response = requests.get("https://api.openweathermap.org/data/2.5/weather",params = {
        "q": city,
        "appid": "399871d262777e04375a1aea5f67f442",
        "units": "metric",
        "lang": "fa"
        },timeout=5)
    return JsonResponse(response.json())



class SignupView(FormView):
    template_name = "registration/signup.html"
    form_class = SignupForm
    success_url = reverse_lazy("todo:task_list")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
