from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import connection

from .models import Author, Book
from .forms import AuthorForm, BookForm


# ─── helpers ─────────────────────────────────────────────────────────────────

def dolt_query(sql, params=None):
    """Run a raw SQL query and return rows as a list of dicts."""
    with connection.cursor() as cur:
        cur.execute(sql, params or [])
        cols = [c[0] for c in cur.description]
        return [dict(zip(cols, row)) for row in cur.fetchall()]


def dolt_execute(sql, params=None):
    """Run a raw SQL statement (no return rows needed)."""
    with connection.cursor() as cur:
        cur.execute(sql, params or [])


# ─── home ─────────────────────────────────────────────────────────────────────

def home(request):
    authors = Author.objects.prefetch_related('books').all()
    books = Book.objects.select_related('author').all()

    # Detect drift: books whose author_name differs from Author.name
    drifted = Book.objects.raw(
        """
        SELECT b.id, b.title, b.author_name AS book_author_name, a.name AS canonical_name
        FROM library_book b
        JOIN library_author a ON b.author_id = a.id
        WHERE b.author_name != a.name
        """
    )

    return render(request, 'library/home.html', {
        'authors': authors,
        'books': books,
        'drifted': list(drifted),
    })


# ─── authors ──────────────────────────────────────────────────────────────────

def author_create(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            author = form.save()
            dolt_execute("CALL DOLT_COMMIT('-Am', %s)", [f"Add author: {author.name}"])
            messages.success(request, f'Author "{author.name}" added and committed to Dolt.')
            return redirect('home')
    else:
        form = AuthorForm()
    return render(request, 'library/form.html', {'form': form, 'title': 'Add Author'})


def author_edit(request, pk):
    author = get_object_or_404(Author, pk=pk)
    old_name = author.name
    if request.method == 'POST':
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            author = form.save()
            # Sync denormalised field on all related books
            if author.name != old_name:
                Book.objects.filter(author=author).update(author_name=author.name)
            dolt_execute("CALL DOLT_COMMIT('-Am', %s)", [f"Update author: {author.name}"])
            messages.success(request, f'Author updated and committed.')
            return redirect('home')
    else:
        form = AuthorForm(instance=author)
    return render(request, 'library/form.html', {'form': form, 'title': 'Edit Author'})


def author_delete(request, pk):
    author = get_object_or_404(Author, pk=pk)
    if request.method == 'POST':
        name = author.name
        author.delete()
        dolt_execute("CALL DOLT_COMMIT('-Am', %s)", [f"Delete author: {name}"])
        messages.success(request, f'Author "{name}" deleted.')
        return redirect('home')
    return render(request, 'library/confirm_delete.html', {'object': author, 'type': 'Author'})


# ─── books ────────────────────────────────────────────────────────────────────

def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            # Auto-fill author_name from the FK if not provided
            if book.author and not book.author_name:
                book.author_name = book.author.name
            book.save()
            dolt_execute("CALL DOLT_COMMIT('-Am', %s)", [f"Add book: {book.title}"])
            messages.success(request, f'Book "{book.title}" added and committed to Dolt.')
            return redirect('home')
    else:
        form = BookForm()
    return render(request, 'library/form.html', {'form': form, 'title': 'Add Book'})


def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save()
            dolt_execute("CALL DOLT_COMMIT('-Am', %s)", [f"Update book: {book.title}"])
            messages.success(request, 'Book updated and committed.')
            return redirect('home')
    else:
        form = BookForm(instance=book)
    return render(request, 'library/form.html', {'form': form, 'title': 'Edit Book'})


def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        title = book.title
        book.delete()
        dolt_execute("CALL DOLT_COMMIT('-Am', %s)", [f"Delete book: {title}"])
        messages.success(request, f'Book "{title}" deleted.')
        return redirect('home')
    return render(request, 'library/confirm_delete.html', {'object': book, 'type': 'Book'})


# ─── Dolt version-control views ───────────────────────────────────────────────

def dolt_log(request):
    rows = dolt_query("SELECT * FROM DOLT_LOG() LIMIT 50")
    return render(request, 'library/dolt_log.html', {'rows': rows})


def dolt_diff(request):
    # Show diff of working set vs HEAD for both tables
    author_diff = dolt_query(
        "SELECT * FROM DOLT_DIFF_SUMMARY('HEAD', 'WORKING', 'library_author')"
    )
    book_diff = dolt_query(
        "SELECT * FROM DOLT_DIFF_SUMMARY('HEAD', 'WORKING', 'library_book')"
    )
    return render(request, 'library/dolt_diff.html', {
        'author_diff': author_diff,
        'book_diff': book_diff,
    })


def fix_drift(request):
    """Sync all Book.author_name values to match Author.name, then commit."""
    if request.method == 'POST':
        with connection.cursor() as cur:
            cur.execute(
                """
                UPDATE library_book b
                JOIN library_author a ON b.author_id = a.id
                SET b.author_name = a.name
                WHERE b.author_name != a.name
                """
            )
            updated = cur.rowcount
        dolt_execute("CALL DOLT_COMMIT('-Am', %s)", ["Fix author_name drift across tables"])
        messages.success(request, f'Fixed {updated} drifted book(s) and committed.')
    return redirect('home')
