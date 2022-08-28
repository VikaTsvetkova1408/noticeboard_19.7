from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from .models import Person, Notice, Category, Rejoinder
from .filters import NoticeCategoryFilter


class CoreIndex(ListView):
    model = Notice
    ordering = 'timestamp'
    paginate_by = 20
    template_name = 'core/index.html'
    context_object_name = 'notice_list'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        context['categories'] = categories

    def get_queryset(self):
        qs = super().get_queryset()
        # qs = qs.filter(type=self.kwargs['notice_category'])
        self.filterset = NoticeCategoryFilter(self.request.GET, qs)
        return self.filterset.qs

