from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from .models import Book
from .forms import BookForm

# Create your views here.
def home(request):
    return render(request, 'myapp/home.html')

def book_list(request):
    books = Book.objects.all()
    return render(request, 'myapp/book_list.html', {'books' : books})

def book_detail(request, pk=None):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'myapp/book_detail.html', {'book' : book})

def book_form(request, pk=None):
    if pk:  # pkが指定されている場合、編集モード
        book = get_object_or_404(Book, pk=pk)
        form = BookForm(instance=book)
    else:  # pkがない場合、新規作成モード
        book = None
        form = BookForm()

    if request.method == 'POST':  # POSTリクエストの場合、フォームを保存
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('book_list'))  # リダイレクト

    # GETリクエストの場合、フォームを表示
    return render(request, 'myapp/book_form.html', {'form': form})
        