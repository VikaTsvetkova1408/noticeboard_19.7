from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, TemplateView, DeleteView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from .models import Person, Notice, Category, Rejoinder
from .filters import NoticeCategoryFilter
from .forms import NoticeForm, RejoinderForm


@method_decorator(ensure_csrf_cookie, name='dispatch')
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


class NoticeDelete(LoginRequiredMixin, DeleteView):
    model = Notice
    template_name = 'core/notice_delete.html'
    success_url = reverse_lazy('core:notice_index')

    def get_object(self, **kwargs):
        obj: Notice = super().get_object(**kwargs)
        author = Person.objects.filter(user=self.request.user).first()
        if author != obj.author:
            raise PermissionDenied
        return obj


class NoticeDetail(DetailView):
    model = Notice
    template_name = 'core/notice_detail.html'

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'notice#{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'notice#{self.kwargs["pk"]}', obj)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']

        form = RejoinderForm()
        notice = get_object_or_404(Notice, pk=pk)
        rejoinders = notice.rejoinder_set.all()

        context['notice'] = notice
        context['rejoinders'] = rejoinders
        context['rejoinder_form'] = form

        return context

    def post(self, *args, **kwargs):
        form = RejoinderForm(self.request.POST)
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)

        notice = Notice.objects.filter(id=self.kwargs['pk']).first()
        rejoinders = notice.rejoinder_set.all()

        context['notice'] = notice
        context['rejoinders'] = rejoinders
        context['rejoinder_form'] = form

        if form.is_valid():
            author = Person.objects.filter(user=self.request.user).first()
            if not author:
                raise ObjectDoesNotExist('Unknown user')
            content = form.cleaned_data['content']
            rejoinder = Rejoinder.objects.create(author=author, content=content, notice=notice)
            form = RejoinderForm()
            context['rejoinder_form'] = form
            return self.render_to_response(context=context)

        return self.render_to_response(context=context)


class RejoinderDelete(LoginRequiredMixin, DeleteView):
    template_name = 'core/rejoinder_delete.html'
    model = Rejoinder

    def get_object(self, **kwargs):
        obj: Rejoinder = super().get_object(**kwargs)
        person = Person.objects.filter(user=self.request.user).first()
        notice: Notice = obj.notice
        if obj.author != person or notice.author != person:
            raise PermissionDenied
        return obj


class PersonProfile(LoginRequiredMixin, TemplateView):
    template_name = 'core/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        person = Person.objects.filter(user=self.request.user).first()
        person_notice_list = Notice.objects.filter(author=person).annotate(rej_count=Count('rejoinder'))
        context['person_notice_list'] = person_notice_list
        return context
