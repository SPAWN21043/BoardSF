from django_filters import FilterSet, DateFilter, CharFilter
from .models import Posts, Responses
from django.forms.widgets import SelectDateWidget


class SearchFilter(FilterSet):
    post = CharFilter(field_name='post__header', label='По объявлениям')
    user = CharFilter(field_name='user__username', label='По автору')
    status = CharFilter(field_name='status', label='По статусу')

    class Meta:
        model = Responses
        fields = {'post', 'user', 'status'}
