from django.contrib import admin

from .models import Person, Notice, Category, Rejoinder


admin.site.register(Person)
admin.site.register(Notice)
admin.site.register(Category)
admin.site.register(Rejoinder)
