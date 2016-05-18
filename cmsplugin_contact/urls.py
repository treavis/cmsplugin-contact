# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns
from .views import ContactFormAjaxView


urlpatterns = i18n_patterns('',
    url(r'^multi_form/$', ContactFormAjaxView.as_view(), name='multi_form'),
)
