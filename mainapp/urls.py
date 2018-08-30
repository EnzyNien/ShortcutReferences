from django.urls import include, re_path, path
from mainapp import views

app_name = 'mainapp'

urlpatterns = [
    re_path(r'^$', views.main, name='main'),
    path('shortcut/<url>', views.shortcut, name='shortcut'),
    path('add_url/', views.add_url, name='add_url'),
]


