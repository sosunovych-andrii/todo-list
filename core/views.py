from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic

from core.models import Task, Tag

class IndexView(generic.ListView):
    model = Task
    template_name = "core/index.html"
    context_object_name = "tasks"
    paginate_by = 2

    def get_queryset(self):
        return (
            super().get_queryset()
            .prefetch_related("tag")
            .order_by("is_completed", "-datetime")
        )

class TaskCreateView(generic.CreateView):
    model = Task
    fields = ("content", "deadline", "tag")
    template_name = "core/task_create.html"
    context_object_name = "task"
    success_url = reverse_lazy("core:index")


class TaskUpdateView(generic.UpdateView):
    model = Task
    fields = ("content", "deadline", "tag")
    template_name = "core/task_update.html"
    context_object_name = "task"
    success_url = reverse_lazy("core:index")


class TaskDeleteView(generic.DeleteView):
    model = Task
    template_name = "core/task_delete.html"
    context_object_name = "task"
    success_url = reverse_lazy("core:index")


class TagListView(generic.ListView):
    model = Tag
    template_name = "core/tag_list.html"
    context_object_name = "tags"
    paginate_by = 4


class TagCreateView(generic.CreateView):
    model = Tag
    fields = ("name",)
    template_name = "core/tag_create.html"
    context_object_name = "tag"
    success_url = reverse_lazy("core:tag-list")


class TagUpdateView(generic.UpdateView):
    model = Tag
    fields = ("name",)
    template_name = "core/tag_update.html"
    context_object_name = "tag"
    success_url = reverse_lazy("core:tag-list")


class TagDeleteView(generic.DeleteView):
    model = Tag
    template_name = "core/tag_delete.html"
    context_object_name = "tag"
    success_url = reverse_lazy("core:tag-list")


class ToggleTaskCompletionView(generic.View):
    def post(self, request: HttpRequest, pk: int, action: str) -> HttpResponseRedirect:
        task = get_object_or_404(Task, pk=pk)
        if action == "complete":
            task.is_completed = True
        elif action == "uncomplete":
            task.is_completed = False
        else:
            return redirect("/")
        task.save()
        return redirect(request.META.get("HTTP_REFERER", "/"))
