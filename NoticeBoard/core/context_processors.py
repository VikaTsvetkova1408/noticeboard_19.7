from django.db.models import Count
from .models import Category


def category(request):
    return {
        'category_list': Category.objects.annotate(notice_count=Count('notice')),
        'category_current': request.GET.get('category')
    }
