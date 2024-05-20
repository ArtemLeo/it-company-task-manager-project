from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from task_manager.forms import PositionForm, WorkerCreationForm, WorkerUpdateForm
from task_manager.models import TaskType, Position, Worker, Task


@login_required
def index(request):
    """View function for the home page of the site"""
    num_workers = Worker.objects.count()
    num_positions = Position.objects.count()
    num_task_types = TaskType.objects.count()

    context = {
        "num_workers": num_workers,
        "num_positions": num_positions,
        "num_task_types": num_task_types,
    }

    return render(request, "task_manager/index.html", context=context)


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    context_object_name = "task_type_list"
    template_name = "task_manager/task_type_list.html"
    paginate_by = 10
    queryset = TaskType.objects.select_related("tasks")


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("task_manager:task-type-list")


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("task_manager:task-type-list")


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    success_url = reverse_lazy("task_manager:task-type-list")


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    paginate_by = 10
    queryset = Position.objects.select_related("workers")


class PositionDetailView(LoginRequiredMixin, generic.DetailView):
    model = Position


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    form_class = PositionForm
    success_url = reverse_lazy("task_manager:position-list")


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    form_class = PositionForm
    success_url = reverse_lazy("task_manager:position-list")


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    success_url = reverse_lazy("task_manager:position-list")


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    paginate_by = 10


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    queryset = Worker.objects.all().prefetch_related("tasks")


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm
    success_url = reverse_lazy("task_manager:worker-detail")


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerUpdateForm
    success_url = reverse_lazy("task_manager:worker-detail")


class DriverDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("task_manager:worker-list")
