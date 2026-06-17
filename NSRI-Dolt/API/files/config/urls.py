from django.urls import path
from library import views

urlpatterns = [
    path('', views.home, name='home'),

    # Authors
    path('authors/new/', views.author_create, name='author_create'),
    path('authors/<int:pk>/edit/', views.author_edit, name='author_edit'),
    path('authors/<int:pk>/delete/', views.author_delete, name='author_delete'),

    # Books
    path('books/new/', views.book_create, name='book_create'),
    path('books/<int:pk>/edit/', views.book_edit, name='book_edit'),
    path('books/<int:pk>/delete/', views.book_delete, name='book_delete'),

    # Dolt
    path('dolt/log/', views.dolt_log, name='dolt_log'),
    path('dolt/diff/', views.dolt_diff, name='dolt_diff'),
    path('dolt/fix-drift/', views.fix_drift, name='fix_drift'),
]
