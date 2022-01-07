from django.contrib import admin
from .models import Date, Expense, Category

admin.site.register(Date)
admin.site.register(Category)
admin.site.register(Expense)