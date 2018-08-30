from django.contrib import admin
from django.urls import include, re_path, path
from django.conf import settings
from mainapp import views
admin.autodiscover()


urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    path('', include('mainapp.urls', namespace='mainapp')),
]

