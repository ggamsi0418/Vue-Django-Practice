from django.shortcuts import render
from django.views.generic import TemplateView


class TodoTV(TemplateView):
    template_name = "todo/todo_index.html"
