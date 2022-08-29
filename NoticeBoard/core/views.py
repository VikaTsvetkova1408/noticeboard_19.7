from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseBadRequest, HttpResponseNotAllowed
from django.views.generic import TemplateView, ListView, CreateView
from django.db.models import Count
from .models import Person, Notice, Category, Rejoinder
from .filters import NoticeCategoryFilter
from .forms import NoticeForm, RejoinderForm


class CoreIndex(ListView):
    model = Notice
    ordering = 'timestamp'
    paginate_by = 20
    template_name = 'core/index.html'
    context_object_name = 'notice_list'

    def get_queryset(self):
        qs = super().get_queryset()
        self.filterset = NoticeCategoryFilter(self.request.GET, qs)
        return self.filterset.qs


class NoticeAdd(LoginRequiredMixin, CreateView):
    form_class = NoticeForm
    model = Notice
    template_name = 'core/notice_add.html'

    def form_valid(self, form):
        notice = form.save(commit=False)
        notice.author = Person.objects.filter(user=self.request.user).first()
        return super().form_valid(form)

    # def get(self, request, *args, **kwargs):
    #     return HttpResponseNotAllowed('Method not allowed')


