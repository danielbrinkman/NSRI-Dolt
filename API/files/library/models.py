from django.db import models
from django.utils import timezone


class Author(models.Model):
    """
    Canonical author record.
    'name' is the shared field that also lives on Book.author_name.
    """
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    birth_year = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Library(models.Model):
    """A physical or logical library that can own books."""
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=300, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Book record.
    'author_name' is intentionally denormalised (duplicated from Author.name)
    to demonstrate a shared field across two tables.
    """
    title = models.CharField(max_length=300)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='books')
    # Denormalised copy – the "shared" field this demo is built around
    author_name = models.CharField(max_length=200)
    published_year = models.IntegerField(null=True, blank=True)
    isbn = models.CharField(max_length=20, blank=True)
    library = models.ForeignKey(
        'Library', null=True, blank=True, on_delete=models.PROTECT, related_name='books'
    )

    class Meta:
        ordering = ['title']

    def __str__(self):
        return f"{self.title} ({self.author_name})"


class DisplayCopy(models.Model):
    """A display event that shows a collection of books.
    
    A display has a title (e.g., "Summer Reading") and a library where it runs.
    Books can be added/removed from a display without affecting the original Book records.
    """
    title = models.CharField(max_length=300)
    library = models.ForeignKey(Library, on_delete=models.PROTECT, related_name='displays')
    books = models.ManyToManyField(Book, related_name='on_display')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-start_date']

    def is_active(self):
        return self.end_date is None

    def __str__(self):
        return f"Display: {self.title} @ {self.library}"
