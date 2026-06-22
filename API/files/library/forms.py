from django import forms
from .models import Author, Book, Library, DisplayCopy


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'bio', 'birth_year']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
        }


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'author_name', 'published_year', 'isbn', 'library']
        help_texts = {
            'author_name': 'Denormalised copy of the author name (shared field demo).',
        }


class LibraryForm(forms.ModelForm):
    class Meta:
        model = Library
        fields = ['name', 'location']


class DisplayCopyForm(forms.ModelForm):
    class Meta:
        model = DisplayCopy
        fields = ['title', 'library']
