from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^results/$', TemplateView.as_view(template_name="results.html"), name='results'),
    url(r'^howto/$', TemplateView.as_view(template_name="howto.html"), name='howto'), 
    url(r'^about/$', TemplateView.as_view(template_name="about.html"), name='about'),  
]