from django.urls import path
from .views import like_by_id, upload, create_channel, home,watch_by_id, like_by_id, dislike_by_id, save_by_id, comment_by_id, subscribe_by_id,delete_by_id,admin,history,library,search

urlpatterns = [

    path('upload/', upload, name='upload'),
    path('create-channel/', create_channel, name='create-channel'),
    path('', home, name='home'),
    path('watch/<int:id>/', watch_by_id, name='watch'),
    path('like/<int:id>/', like_by_id, name='like'),
    path('dislike/<int:id>/', dislike_by_id, name='dislike'),
    path('save/<int:id>/', save_by_id, name='save'),
    path('comment/<int:id>/', comment_by_id, name='comment'),
    path('subscribe/<int:id>/', subscribe_by_id, name='subscribe'),
    path('delete/<int:id>/', delete_by_id, name='delete'),
    path('admin/', admin, name='admin'),
    path('history/', history, name='history'),
    path('library/', library, name='library'),
    path('search/',search,name='search')
    
    
]
