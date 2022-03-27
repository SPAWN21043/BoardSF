from django.forms import ModelForm, CharField, Textarea
from Post.models import Posts, Responses


class PostsForm(ModelForm):
    class Meta:
        model = Posts
        fields = ['header', 'category', 'content', 'user']


class ResponseForm(ModelForm):
    text = CharField()

    class Meta:
        model = Responses
        fields = ['text']
