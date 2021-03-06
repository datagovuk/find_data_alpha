from django.views.generic import TemplateView
from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', views.home, name='home'),
    url(r'^cookies$', TemplateView.as_view(template_name='cookies.html'), name='cookies'),
    url(r'^download/(?P<dataset_id>[0-9a-z-]+)/(?P<resource_id>[0-9a-z-]+)$',
        views.download, name='download'),
    url(r'^dataset/', include('dataset.urls')),
    url(r'^stats/', include('stats.urls')),
]
