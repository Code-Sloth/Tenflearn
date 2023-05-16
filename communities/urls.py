from django.urls import path, include
from . import views
app_name = 'communities'
urlpatterns = [
# 댓글 CRUD
    path('comments/', views.comment, name='comment_index'),
    path('comments/<int:comment_pk>/', views.comment_detail, name='comment_detail'),
    path('comments/create/', views.comment_create, name='comment_create'),
    path('comments/<int:comment_pk>/update/', views.comment_update, name='comment_update'),
    path('comments/<int:comment_pk>/delete/', views.comment_delete, name='comment_delete'),
    path('comments/<int:comment_pk>/likes/', views.comment_like, name='comment_like'),

# 대댓글 CRD
    path('comments/<int:comment_pk>/recomments/create/', views.recomment_create, name='recomment_create'),
    path('comments/<int:comment_pk>/recomments/<int:recomment_pk>/delete/', views.recomment_delete, name='recomment_delete'),
    path('comments/<int:comment_pk>/recomments/<int:recomment_pk>/likes/', views.recomment_like, name='recomment_like'),

# 리뷰 CRD 
    path('reviews/', views.review, name='inflearn_index'),

]


