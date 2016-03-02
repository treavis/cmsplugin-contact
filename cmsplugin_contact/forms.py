from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.html import conditional_escape, format_html
#import settings
from cmsplugin_contact.nospam.forms import HoneyPotForm, RecaptchaForm, AkismetForm

class BootstrapWidget(forms.Widget):
    def __init__(self, wrap_widget_cls, div_class_add='', *args, **kwargs):
        kwargs['attrs'] = kwargs.get('attrs', {})
        kwargs['attrs']['class'] = 'form-control'
        self.wrap_widget = wrap_widget_cls(kwargs['attrs'])
        self.div_class_add = div_class_add
        super(BootstrapWidget, self).__init__(*args, **kwargs)
    
    def render(self, name, value, attrs=None):
        return self.wrap_widget.render(name, value, attrs)
  
class ContactForm(forms.Form):
    email = forms.EmailField(label=_("Email"), required=True, widget=BootstrapWidget(forms.EmailInput, 'email', attrs={'autocomplete':'off'}))
    content = forms.CharField(label=_("Message"), required=True, widget=BootstrapWidget(forms.Textarea, 'textarea'))

    template = "cmsplugin_contact/contact.html"
  
class HoneyPotContactForm(HoneyPotForm):
    pass

class AkismetContactForm(AkismetForm):
    akismet_fields = {
        'comment_author_email': 'email',
        'comment_content': 'content'
    }
    akismet_api_key = None
    

class RecaptchaContactForm(RecaptchaForm):
    recaptcha_public_key = None
    recaptcha_private_key = None
    recaptcha_theme = None