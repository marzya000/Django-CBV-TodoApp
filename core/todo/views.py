from django.shortcuts import get_object_or_404, redirect
from .models import Task
from .forms import TaskForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import View



# Create your views here.



class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "todo/task_list.html"

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
        

class TaskListApi(TemplateView):
    template_name = "todo/task_list_api.html"



class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("todo:task_list")
    template_name = "todo/task_form.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("todo:task_list")
    template_name = "todo/task_form.html"

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class TaskComplete(LoginRequiredMixin, View):
    model = Task
    success_url = reverse_lazy('todo:task_list')

    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, id=kwargs['pk'], user=request.user)
        task.complete = not task.complete
        task.save()
        messages.success(request, f'Task marked as {"Done" if task.complete else "Waiting"}')
        return redirect('todo:task_list')

    def get(self, request, *args, **kwargs):
        messages.warning(request, "You cannot access this URL directly.")
        return redirect('todo:task_list')



class TaskDelete(LoginRequiredMixin, DeleteView): 
    model = Task
    context_object_name = "task"
    success_url = reverse_lazy("todo:task_list")
    template_name = "todo/task_confirm_delete.html"

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

            
        
