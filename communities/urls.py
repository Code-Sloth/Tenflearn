from django.urls import path, include
from . import views
app_name = 'communities'
urlpatterns = [
# 댓글 crud 
    path('comments/', views.comment, name='comment_index'),
    path('comments/<int:comment_pk>/', views.comment_detail, name='comment_detail'),
    path('comments/create/', views.comment_create, name='comment_create'),
    path('comments/<int:comment_pk>/update/', views.comment_update, name='comment_update'),
    path('comments/<int:comment_pk>/delete/', views.comment_delete, name='comment_delete'),

# 대댓글 crd
    path('comments/<int:comment_pk>/recomments/', views.recomment, name='recomment'),
    path('comments/<int:comment_pk>/recomments/create/', views.recomment_create, name='recomment_create'),
    path('comments/<int:comment_pk>/recomments/<int:recomment_pk>/delete/', views.recomment_delete, name='recomment_delete'),

#리뷰 crd 
    path('reviews/', views.reviews, name='inflearn_index'),
    path('reviews/create/', views.review_create, name='review_create'),
    path('reviews/<int:review_pk>/delete/', views.review_delete, name='review_delete'),



]


