from django_filters import FilterSet
from .models import Notice


class NoticeCategoryFilter(FilterSet):
    class Meta:
        model = Notice
        fields = ['category']

