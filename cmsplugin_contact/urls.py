# -*- coding: utf-8 -*-

from django.conf.urls import url
from .views import ContactFormAjaxView


urlpatterns = [
    url(r'^multi_form/$', ContactFormAjaxView.as_view(), name='multi_form'),
]
