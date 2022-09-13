from django.urls import path

from .views import (
    PostView,
    PostDetailView,
    CategoryDetailView,
    AddCommentView,
    LikeView,
    AddReplyCommentView,
    AddPostView,
    AddCategoryView,
    UpdatePostView,
    DeletePostView
)

urlpatterns = [
    path('', PostView.as_view(), name='home'),

    path('add-post/', AddPostView.as_view(), name='add-post'),
    path('add-category/', AddCategoryView.as_view(), name='add-category'),
    path('post/edit/<int:pk>', UpdatePostView.as_view(), name='update-post'),
    path('post/<int:pk>/delete', DeletePostView.as_view(), name='post-delete'),
    path('category/<int:pk>', CategoryDetailView.as_view(), name='category'),
    path('<str:slug>', PostDetailView.as_view(), name='post-view'),
    path('post/<int:pk>/comment', AddCommentView.as_view(), name='add-comment'),
    path('reply-comment/<int:pk>', AddReplyCommentView.as_view(), name='reply-comment'),
    path('like/', LikeView, name='like-post'),
]
