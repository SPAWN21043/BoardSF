from django.forms import ModelForm, CharField, forms
from Post.models import Posts, Responses
from django import forms


class PostsForm(ModelForm):
    class Meta:
        model = Posts
        fields = ['header', 'category', 'content', 'author']
        widgets = {'author': forms.HiddenInput(), }


class ResponseForm(ModelForm):
    text = CharField()

    class Meta:
        model = Responses
        fields = ['text']
