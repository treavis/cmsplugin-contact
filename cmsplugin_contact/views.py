# -*- coding: utf-8 -*-
# Django 1.6

import json
from django.utils.functional import Promise
from django.utils.encoding import force_text
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import FormView

from cms.models.pagemodel import Page
from cms.models.pluginmodel import CMSPlugin
from cms.plugin_pool import plugin_pool

from .forms import ContactForm

#
# From: https://docs.djangoproject.com/en/1.6/topics/class-based-views/generic-editing/#ajax-example
#
class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    
    def render_to_json_response(self, context, **response_kwargs):
        class LazyEncoder(DjangoJSONEncoder):
            def default(self, obj):
                if isinstance(obj, Promise):
                    return force_text(obj)
                return super(LazyEncoder, self).default(obj)
        data = json.dumps(context, cls=LazyEncoder)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return self.render_to_json_response(form.errors)  # , status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'ok': 'ok',
            }
            return self.render_to_json_response(data)
        else:
            return response


#
# This is used from the ContactPlugin, so could be anywhere on the site. It is
# submitted via AJAX and shouldn't take the user off the page.
#
class ContactFormAjaxView(AjaxableResponseMixin, FormView):
    form_class = ContactForm
    http_method_names = [u'post']  # Not interested in any GETs here...
    template_name = 'cmsplugin_contact/contact.html'

    def get_plugin(self):
        # this relies on existance of self.request (see def post)
        plugin_inst_id = int(self.request.POST['plugininstance'])
        plugin_model = CMSPlugin.objects.get(pk=plugin_inst_id)
        self._plugin_inst, self._plugin = plugin_model.get_plugin_instance()

    def plugin(self):
        if not hasattr(self, '_plugin'):
            self.get_plugin()
        return self._plugin
    plugin = property(plugin)

    def plugin_inst(self):
        if not hasattr(self, '_plugin_inst'):
            self.get_plugin()
        return self._plugin_inst
    plugin_inst = property(plugin_inst)

    def get_form_class(self):
        return self.plugin.get_contact_form_class(self.plugin_inst)

    def get_form(self, form_class):
        return self.plugin.get_contact_form(form_class, self.plugin_inst, self.request)

    #
    # NOTE: Even though this will never be used, the FormView requires that
    # either the success_url property or the get_success_url() method is
    # defined. So, let use the sensible thing and set it to the page where
    # this plugin is coming from.
    #
    def get_success_url(self):
        return self.request.path

    def form_valid(self, form):
        # AjaxableResponseMixin expects our contact object to be 'self.object'.
        instance = self.plugin_inst
        self.plugin.send(form, instance.form_name, instance.site_email, attachments=self.request.FILES)
        return super(ContactFormAjaxView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.request = request
        return super(ContactFormAjaxView, self).post(request, *args, **kwargs)
