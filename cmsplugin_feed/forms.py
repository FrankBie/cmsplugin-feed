from django.forms.models import ModelForm
from django import forms

from cmsplugin_feed.models import Feed

class FeedForm(ModelForm):
    class Meta:
        model = Feed