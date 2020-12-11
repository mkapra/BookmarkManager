from django.urls import path

from . import views

app_name = 'bookmarks'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('archive/', views.archive_bookmarks, name='archive'),
    path('<int:bookmark_id>/archive', views.archive_bookmark, name='archive_bookmark'),
    path('<int:tag_id>/', views.tag, name='tag'),
    path('<int:bookmark_id>/delete', views.delete_bookmark, name='delete_bookmark'),
]