from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('my-movies/', views.my_movies, name='my_movies'),

    path('movies/', views.movie_list, name='movie_list'),
    path('movies/create/', views.MovieCreateView.as_view(), name='movie_create'),
    path('movies/<int:pk>/', views.movie_detail, name='movie_detail'),
    path('movies/<int:pk>/update/', views.MovieUpdateView.as_view(), name='movie_update'),
    path('movies/<int:pk>/delete/', views.MovieDeleteView.as_view(), name='movie_delete'),
    path('movies/<int:pk>/favorite/', views.add_favorite, name='add_favorite'),
    path('movies/<int:pk>/unfavorite/', views.remove_favorite, name='remove_favorite'),
    path('movies/<int:pk>/review/', views.write_review, name='write_review'),

    path('reviews/<int:pk>/edit/', views.edit_review, name='edit_review'),
    path('reviews/<int:pk>/delete/', views.delete_review, name='delete_review'),

    path('directors/', views.director_list, name='director_list'),
    path('directors/create/', views.DirectorCreateView.as_view(), name='director_create'),
    path('directors/<int:pk>/', views.director_detail, name='director_detail'),
    path('directors/<int:pk>/update/', views.DirectorUpdateView.as_view(), name='director_update'),
    path('directors/<int:pk>/delete/', views.DirectorDeleteView.as_view(), name='director_delete'),

    path('genres/', views.genre_list, name='genre_list'),
    path('genres/<int:pk>/', views.genre_detail, name='genre_detail'),

    path('themes/', views.theme_list, name='theme_list'),
    path('themes/<int:pk>/', views.theme_detail, name='theme_detail'),

    path('reviews/', views.review_list, name='review_list'),
    path('reviews/<int:pk>/', views.review_detail, name='review_detail'),

    path('comments/', views.comment_list, name='comment_list'),
    path('comments/<int:pk>/', views.comment_detail, name='comment_detail'),

    path('favorites/', views.favorite_list, name='favorite_list'),
    path('favorites/<int:pk>/', views.favorite_detail, name='favorite_detail'),
    path('recommend_movie/', views.recommend_movie, name='recommend_movie'),
]
