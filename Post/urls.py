from django.urls import path
from .views import PostsList, PostDetail, CreatePost, PrivateList, UpdatePostList, PostUpdate, sub_category
from Post import views


urlpatterns = [
    path('', PostsList.as_view()),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('create/', CreatePost.as_view()),
    path('private/', PrivateList.as_view()),
    path('delete/<int:pk>/', views.delete_responses),
    path('update/<int:pk>/', views.public_responses),
    path('post_update/', UpdatePostList.as_view(), name='update_post'),
    path('upsate_pos/<int:pk>/', PostUpdate.as_view(), name='up_post'),
    path('subscribe/', sub_category),

]
