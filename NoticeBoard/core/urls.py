from django.urls import path, include
from django.views.decorators.cache import cache_page
from . import views


app_name = 'core'

urlpatterns = [
    path('', views.CoreIndex.as_view(), name='core_notice_index'),
    path('add', views.NoticeAdd.as_view(), name='core_notice_add')
    # path('notice/<int:pk>', )
]
