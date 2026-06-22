from django.contrib import admin
from .models import Author, Book, Library, DisplayCopy

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'birth_year']
    search_fields = ['name']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author_name', 'author', 'published_year', 'library']
    search_fields = ['title', 'author_name']
    list_filter = ['author', 'library']

@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ['name', 'location']
    search_fields = ['name']

@admin.register(DisplayCopy)
class DisplayCopyAdmin(admin.ModelAdmin):
    list_display = ['title', 'library', 'start_date', 'end_date']
    list_filter = ['library', 'start_date']
    filter_horizontal = ['books']
