from django.db import models


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

    class Meta:
        ordering = ['title']

    def __str__(self):
        return f"{self.title} ({self.author_name})"
    
class Member(models.Model):
    name = models.CharField(max_length=200)
    card_number = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Checkout(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    checkout_date = models.DateTimeField(auto_now_add=True)
    returned = models.BooleanField(default=False)

    class Meta:
        # This prevents a member from ever having duplicate checkout records for the same book
        constraints = [
            models.UniqueConstraint(
                fields=['member', 'book'], 
                name='unique_member_book_checkout'
            )
        ]

    def __str__(self):
        return f"{self.member.name} checked out {self.book.title}"
