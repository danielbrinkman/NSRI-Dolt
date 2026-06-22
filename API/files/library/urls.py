from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Authors
    path('authors/new/', views.author_create, name='author_create'),
    path('authors/<int:pk>/edit/', views.author_edit, name='author_edit'),
    path('authors/<int:pk>/delete/', views.author_delete, name='author_delete'),

    # Libraries
    path('libraries/new/', views.library_create, name='library_create'),
    path('libraries/<int:pk>/edit/', views.library_edit, name='library_edit'),
    path('libraries/<int:pk>/delete/', views.library_delete, name='library_delete'),

    # Books
    path('books/new/', views.book_create, name='book_create'),
    path('books/<int:pk>/edit/', views.book_edit, name='book_edit'),
    path('books/<int:pk>/delete/', views.book_delete, name='book_delete'),
    path('books/<int:pk>/move/', views.move_book, name='book_move'),
    path('books/<int:pk>/display/', views.make_display, name='book_display'),

    # Displays
    path('displays/new/', views.display_create, name='display_create'),
    path('displays/<int:pk>/edit/', views.display_edit, name='display_edit'),
    path('displays/<int:pk>/delete/', views.display_delete, name='display_delete'),
    path('displays/<int:pk>/end/', views.end_display, name='end_display'),

    # Dolt
    path('dolt/log/', views.dolt_log, name='dolt_log'),
    path('dolt/diff/', views.dolt_diff, name='dolt_diff'),
    path('dolt/fix-drift/', views.fix_drift, name='fix_drift'),
]
