from django.urls import path
from .views import PostsList, PostDetail, CreatePost, PrivateList


urlpatterns = [
    path('', PostsList.as_view()),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('create/', CreatePost.as_view()),
    path('private/', PrivateList.as_view()),
]
