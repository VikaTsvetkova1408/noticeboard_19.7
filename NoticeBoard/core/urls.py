from django.urls import path, include
from django.views.decorators.cache import cache_page
from . import views


app_name = 'core'

urlpatterns = [
    path('', views.CoreIndex.as_view(), name='core_index'),
    # path('notice/<int:pk>', )
]
