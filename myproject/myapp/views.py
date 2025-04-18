from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django import forms
from django.db.models import Q
from .models import Anime, Cast, Staff, Book, Music
from .forms import AnimeForm, AnimeSearchForm, CastSearchForm, StaffSearchForm, BookForm, MusicForm
import logging

logger = logging.getLogger(__name__)
# Create your views here.
def home(request):
    return render(request, 'myapp/home.html')


#anime関連 
def anime_detail(request, pk=None):
    anime = get_object_or_404(Anime, pk=pk)
    casts = Cast.objects.filter(anime = anime).order_by('name')
    return render(request, 'myapp/anime_detail.html', {'anime' : anime, 'casts' : casts})


def anime_edit(request, pk=None):
    anime = get_object_or_404(Anime, pk = pk)
    form = AnimeForm(instance = anime)
    
    if request.method == 'POST':
        form = AnimeForm(request.POST, instance = anime)
        if form.is_valid():
            print(form.cleaned_data)
            anime = form.save(commit = False)
            anime.save()
            
            anime.genre.set(form.cleaned_data.get('genres', []))
            anime.status.set(form.cleaned_data.get('statuses', []))
            anime.value.set(form.cleaned_data.get('values', []))
            
            return HttpResponseRedirect(reverse('anime_detail'))


def anime_search(request):
    anime_form = AnimeSearchForm(request.GET or None, request=request)
    anime_results = None
    field_data = []
    search_query = {}

    if not anime_form.is_valid():
        logger.info("データを受け取れませんでした")
    # Animeフォームの条件追加
    if anime_form.is_valid():
        title = anime_form.cleaned_data.get('title')
        title_kana = anime_form.cleaned_data.get('title_kana')
        media = anime_form.cleaned_data.get('media')
        season_year = anime_form.cleaned_data.get('season_year')
        season_name = anime_form.cleaned_data.get('season_name')
        genres = anime_form.cleaned_data.get('genres')
        statuses = anime_form.cleaned_data.get('statuses')
        values = anime_form.cleaned_data.get('values')
        
    # クエリを個別に構築
        anime_query = Q()
        if title:
            anime_query &= Q(title__icontains=title)
            search_query['title'] = title
        if title_kana:
            anime_query &= Q(title_kana__icontains=title_kana)
            search_query['title_kana'] = title_kana
        if media:
            anime_query &= Q(media__icontains=media)
            search_query['media'] = media
        if season_year:
            anime_query &= Q(season_year__icontains=season_year)
            search_query['season_year'] = season_year
        if season_name:
            anime_query &= Q(season_name__incontains=season_name)
            search_query['season_name'] = season_name
        if genres:
            anime_query &= Q(genre__in=genres)
            search_query['genres'] = genres
        if statuses:
            anime_query &= Q(status__in=statuses)
            search_query['statuses'] = statuses
        if values:
            anime_query &= Q(value__in=values)
            search_query['values'] = values

        # 検索結果を取得
        anime_results = Anime.objects.filter(anime_query).distinct()

    # フィールド情報を収集（検索結果表示用）
        for field in anime_form:
            field_data.append({
                'field': field,
                'is_checkbox': isinstance(field.field.widget, forms.CheckboxSelectMultiple),
                'form_name': 'anime_form',
            })
            
        # 検索結果がある場合
        return render(request, 'myapp/anime_search_results.html', {
            'anime_form': anime_form,
            'anime_results': anime_results,
            'field_data': field_data,
            'search_query': search_query,
        })
        
    for field in anime_form:
        field_data.append({
        'field': field,
        'is_checkbox': isinstance(field.field.widget, forms.CheckboxSelectMultiple),
        'form_name': 'anime_form',
    })
    
    # 検索結果がない場合の処理
    return render(request, 'myapp/anime_search.html', {
        'anime_form': anime_form,
        'anime_results' : anime_results,
        'field_data': field_data,
        'search_query': search_query,
    })




#book関連
def book_list(request):
    books = Book.objects.all()
    return render(request, 'myapp/book_list.html', {'books' : books})

def book_detail(request, pk=None):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'myapp/book_detail.html', {'book' : book})

def book_search(request):
    form = BookForm(request.GET or None, request = request)
    results = None
    field_data = []
    search_query = {}
    
    if not form.is_valid():
        print(form.errors)
        
    if form.is_valid():
        title = form.cleaned_data.get('title')
        author = form.cleaned_data.get('author')
        designer = form.cleaned_data.get('designer')
        types = form.cleaned_data.get('types')
        genres = form.cleaned_data.get('genres')
        statuses = form.cleaned_data.get('statuses')
        values = form.cleaned_data.get('values')
        
        query = Q()
        if title:
            query &= Q(title__icontains = title)
            search_query['title'] = title
        if author:
            query &= Q(author__icontains = author)
            search_query['author'] = author
        if designer:
            query &= Q(designer__icontains = designer)
            search_query['designer'] = designer
        if types:
            query &= Q(type__in = types)
            search_query['types'] = types
        if genres:
            query &= Q(genre__in = genres)
            search_query['genres'] = genres
        if statuses:
            query &= Q(status__in = statuses)
            search_query['statuses'] = statuses
        if values:
            query &= Q(value__in = values)
            search_query['values'] = values
        
        results =  Book.objects.filter(query).distinct()  
        
        for field in form:
            field_data.append({
                'field' : field,
                'is_checkbox' : isinstance(field.field.widget, forms.CheckboxSelectMultiple)
            })
        return render(request, 'myapp/book_search_results.html', {'form' : form, 'results' : results, 'field_data' : field_data, 'search_query' : search_query})
    
    for field in form:
        field_data.append({
            'field' : field,
            'is_checkbox' : isinstance(field.field.widget, forms.CheckboxSelectMultiple)
        })
    return render(request, 'myapp/book_search.html', {'form' : form, 'field_data' : field_data})                                                    

@require_POST
def book_delete(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return redirect('book_list')

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
            print(form.cleaned_data)
            book = form.save(commit=False)
            book.save()
            form.save_m2m()  # この行を追加

            # ManyToManyFieldに手動で関連付けを追加
            book.type.set(form.cleaned_data.get('types', []))
            book.genre.set(form.cleaned_data.get('genres', []))
            book.status.set(form.cleaned_data.get('statuses', []))
            book.value.set(form.cleaned_data.get('values', []))
            
            return HttpResponseRedirect(reverse('book_list'))  # リダイレクト
        

    # 各フィールドの情報を追加
    field_data = []
    for field in form:
        field_data.append({
            'field': field,
            'is_checkbox': isinstance(field.field.widget, forms.CheckboxSelectMultiple)  # チェックボックス判定
        })

    # テンプレートに渡す
    return render(request, 'myapp/book_form.html', {'field_data': field_data})


#music関連
def music_list(request):
    musics = Music.objects.all()
    return render(request, 'myapp/music_list.html', {'musics' : musics})

def music_detail(request, pk=None):
    music = get_object_or_404(Music, pk=pk)
    return render(request, 'myapp/music_detail.html', {'music' : music})

def music_search(request):
    form = MusicForm(request.GET or None, request = request)
    results = None
    field_data = []
    search_query = {}
    
    if not form.is_valid():
        print(form.errors)
    
    if form.is_valid():
        song_name = form.cleaned_data.get('song_name')
        singger = form.cleaned_data.get('singger')
        writer = form.cleaned_data.get('writer')
        sing_writer = form.cleaned_data.get('sing_writer')
        song_write = form.cleaned_data.get('song_write')
        editor = form.cleaned_data.get('editor')
        status = form.cleaned_data.get('status')
        value = form.cleaned_data.get('value')
        
        query = Q()
        if song_name:
            query &= Q(song_name__icontains = song_name)
            search_query['song_name'] = song_name
        if singger:
            query &= Q(singger__icontains = singger)
            search_query['singger'] = singger
        if writer:
            query &= Q(writer__icontains = writer)
            search_query['writer'] = writer
        if sing_writer:
            query &= Q(sing_writer__icontains = sing_writer)
            search_query['sing_writer'] = sing_writer
        if song_write:
            query &= Q(song_write__icontains = song_write)
            search_query['song_write'] = song_write  
        if editor:
            query &= Q(editor__icontains = editor)
            search_query['editor'] = editor 
        if status:
            query &= Q(status_in = status)
            search_query['status'] = status
        if value:
            query &= Q(value_in = value)
            search_query['value'] = value                                                

        results = Music.objects.filter(query).distinct()
        for field in form:
            field_data.append({
                'field' : field,
                'is_checkbox' : isinstance(field.field.widget, forms.CheckboxSelectMultiple)
            })
        
        return render(request, 'myapp/music_search_results.html', 
                      {'form' : form, 'results' : results, 'field_data' : field_data, 'search_query' : search_query})
    
    for field in form:
        field_data.append({
            'field' : field,
            'is_checkbox' : isinstance(field.field.widget, forms.CheckboxSelectMultiple)
        })   
    return render(request, 'myapp/music_search.html', 
                    {'form' : form, 'results' : results, 'field_data' : field_data, 'search_query' : search_query})
    
    
@require_POST
def music_delete(request, music_id):
    music = get_object_or_404(Music, id = music_id)
    music.delete()
    return redirect('music_list')

def music_form(request, pk = None):
    if pk:
        music = get_object_or_404(Music, pk = pk)
        form = MusicForm(instance = music)
    else:
        music = None 
        form = MusicForm()
    
    if request.method == 'POST':
        form = MusicForm(request.POST, instance = music)
        if form.is_valid():
            print(form.cleaned_data)
            music = form.save(commit = False)
            music.save()
            music.status.set(form.cleaned_data.get('status', []))
            music.value.set(form.cleaned_data.get('values', []))
            
            return HttpResponseRedirect(reverse('music_list'))
        
    field_data = []
    for field in form:
        field_data.append({
            'field' : field, 
            'is_checkbox' : isinstance(field.field.widget,
                                       forms.CheckboxSelectMultiple)
        })
        
    return render(request, 'myapp/music_form.html', {'field_data' : field_data})