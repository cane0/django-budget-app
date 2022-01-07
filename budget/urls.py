from django.urls import path
from . import views

urlpatterns = [
    path('', views.date_list, name='list'),
    path('add', views.ProjectCreateView.as_view(), name='add'),
    path('<slug:date_slug>', views.date_detail, name='detail'),
]