from django.urls import path 
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('success', views.success),
    path('login', views.login),
    path('logout', views.logout),
    
    path('drop_menu', views.drop_menu),
    path('search_youtube', views.search_youtube),
    path('review/<str:video_id>', views.view_reviews),
    path('write_review/<str:video_id>', views.view_write),
    path('front_page', views.front_page),
    # path('advanced_search', views.advanced_search),
    path('display_review', views.display_review),
    path('page2/<str:search_term>', views.page2),
    path('page3/<str:search_term>', views.page3),
    path('page4/<str:search_term>', views.page4),
    path('my_reviews', views.my_reviews),
    path('edit_review/<str:review_id>', views.edit_review),
    path('update_review/<str:review_id>', views.update_review),
    path('delete_review/<str:review_id>', views.delete_review),

]