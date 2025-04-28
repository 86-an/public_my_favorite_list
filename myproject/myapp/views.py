from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.core.paginator import Paginator
from django import forms
from django.db.models import Q
from .models import Anime, Cast, Staff, Book, Music
from .forms import AnimeForm, AnimeSearchForm, CastSearchForm, StaffSearchForm, BookForm, MusicForm
import logging
from urllib.parse import urlencode

logger = logging.getLogger(__name__)
# Create your views here.
def home(request):
    return render(request, 'myapp/home.html')

def anime_list(request):
    anime_queryset = Anime.objects.all()
    paginator = Paginator(anime_queryset, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'myapp/anime_list.html', {'page_obj' : page_obj})

#anime関連 (詳細、フォーム、検索)
def anime_detail(request, pk=None):
    anime = get_object_or_404(Anime.objects.prefetch_related('casts', 'staff'), pk=pk)
    return render(request, 'myapp/anime_detail.html', {'anime' : anime})


def anime_form(request, pk=None):
    if pk:  # pkが指定されている場合、編集モード
        anime = get_object_or_404(Anime, pk=pk)
        anime_form = AnimeSearchForm(instance=anime)
    else:  # pkがない場合、新規作成モード
        anime = None
        anime_form = AnimeSearchForm()

    if request.method == 'POST':  # POSTリクエストの場合、フォームを保存
        anime_form = AnimeSearchForm(request.POST, instance=anime)
        if anime_form.is_valid():
            print(anime_form.cleaned_data)
            anime = anime_form.save(commit=False)
            anime.save()
            anime_form.save_m2m()  # この行を追加

            # ManyToManyFieldに手動で関連付けを追加
            anime.genre.set(anime_form.cleaned_data.get('genres', []))
            anime.status.set(anime_form.cleaned_data.get('statuses', []))
            anime.value.set(anime_form.cleaned_data.get('values', []))

            return HttpResponseRedirect(reverse('anime_search'))  # リダイレクト

    # 各フィールドの情報を追加
    field_data = []
    for field in anime_form:
        field_data.append({
            'field': field,
            'name': field.name,
            'is_checkbox': isinstance(field.field.widget, forms.CheckboxSelectMultiple),
            'is_select': isinstance(field.field.widget, forms.Select),
            'form_name': 'anime_form',
        })

    # テンプレートに渡す
    return render(request, 'myapp/anime_form.html', {'field_data': field_data, 'anime': anime}) # 'anime' を追加

@require_POST
def anime_delete(request, anime_id):
    anime = get_object_or_404(Anime, id=anime_id)
    anime.delete()
    return redirect('anime_list')


def anime_search(request):
    anime_form = AnimeSearchForm(request.GET or None, request=request)
    cast_form = CastSearchForm(request.GET or None)
    staff_form = StaffSearchForm(request.GET or None)
    anime_results, cast_results, staff_results = None, None, None
    field_data = []
    search_query = {}
    search_executed = False
    anime_query = Q()

    # アニメ検索処理
    if anime_form.is_valid() and any(anime_form.cleaned_data.values()):
        search_executed = True
        title = anime_form.cleaned_data.get('title')
        title_kana = anime_form.cleaned_data.get('title_kana')
        medias = anime_form.cleaned_data.get('medias')
        season_year = anime_form.cleaned_data.get('season_year')
        season_name = anime_form.cleaned_data.get('season_name')
        genres = anime_form.cleaned_data.get('genres')
        statuses = anime_form.cleaned_data.get('statuses')
        values = anime_form.cleaned_data.get('values')
        
        if title:
            anime_query &= Q(title__icontains=title)
            search_query['title'] = title
        if title_kana:
            anime_query &= Q(title_kana__icontains=title_kana)
            search_query['title_kana'] = title_kana
        if medias:
            anime_query &= Q(media__icontains=medias)
            search_query['medias'] = medias
        if season_year:
            anime_query &= Q(season_year__icontains=medias)
            search_query['season_year'] = season_year
        if season_name:
            anime_query &= Q(season_name__icontains=medias)
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
            
    # キャスト検索処理
    if cast_form.is_valid() and any(cast_form.cleaned_data.values()):
        search_executed = True
        cast_query = Q()
        cast_name = cast_form.cleaned_data.get('cast_name')

        if cast_name:
            cast_query &= Q(name__icontains=cast_name)
            search_query['cast_name'] = cast_name

        cast_results = Cast.objects.filter(cast_query).distinct().order_by('name')

        if cast_results.exists():
            anime_query &= Q(casts__in=cast_results)

    # スタッフ検索処理
    if staff_form.is_valid() and any(staff_form.cleaned_data.values()):
        search_executed = True
        staff_query = Q()
        staff_name = staff_form.cleaned_data.get('staff_name')

        if staff_name:
            staff_query &= Q(name__icontains=staff_name)
            search_query['staff_name'] = staff_name

        staff_results = Staff.objects.filter(staff_query).distinct().order_by('name')

        if staff_results.exists():
            anime_query &= Q(staff__in=staff_results)

    # 検索が実行された場合のみアニメ結果を取得
    if search_executed:
        anime_results = Anime.objects.filter(anime_query).distinct().order_by('title')
        
        # 🔹 ページネーション処理を追加
        paginator = Paginator(anime_results, 15) 
        page_number = request.GET.get('page')
        anime_results = paginator.get_page(page_number)

        current_query = request.GET.copy()
        if 'page' in current_query:
            current_query.pop('page')
        query_string = current_query.urlencode()
        
    # フォームのフィールド情報を収集
    for field in anime_form:
        field_data.append({
            'field': field,
            'is_checkbox': isinstance(field.field.widget, forms.CheckboxSelectMultiple),
            'is_select': isinstance(field.field.widget, forms.Select),
            'form_name': 'anime_form',
        })
    for field in cast_form:
        field_data.append({
            'field': field,
            'is_checkbox': isinstance(field.field.widget, forms.CheckboxSelectMultiple),
            'is_select': isinstance(field.field.widget, forms.Select),
            'form_name': 'cast_form',
        })
    for field in staff_form:
        field_data.append({
            'field': field,
            'form_name': 'staff_form',
        })

    # 結果ページをレンダリング
    if search_executed:
        return render(request, 'myapp/anime_search_results.html', {
            'anime_form': anime_form,
            'cast_form': cast_form,
            'staff_form': staff_form,
            'anime_results': anime_results,  # ページネーションされた結果
            'cast_results': cast_results,
            'staff_results': staff_results,
            'field_data': field_data,
            'search_query': search_query,
            'query_string' : query_string,
        })

    # 検索されていない場合のページ
    return render(request, 'myapp/anime_search.html', {
        'anime_form': anime_form,
        'cast_form': cast_form,
        'staff_form': staff_form,
        'anime_results': anime_results,
        'cast_results': cast_results,
        'field_data': field_data,
        'search_query': search_query,
    })

#book関連（一覧、詳細、削除、検索）
def book_list(request):
    book_queryset = Book.objects.all().order_by("author")
    paginator = Paginator(book_queryset, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'myapp/book_list.html', {'page_obj' : page_obj})

def book_detail(request, pk=None):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'myapp/book_detail.html', {'book' : book})

@require_POST
def book_delete(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return redirect('book_list')

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
        
        results =  Book.objects.filter(query).distinct().order_by('author')  
        paginator = Paginator(results, 30)
        page_number = request.GET.get('page')
        results = paginator.get_page(page_number)
        
        current_query = request.GET.copy()
        if 'page' in current_query:
            current_query.pop('page')
        query_string = current_query.urlencode()
        
        for field in form:
            field_data.append({
                'field' : field,
                'is_checkbox' : isinstance(field.field.widget, forms.CheckboxSelectMultiple)
            })
        return render(request, 'myapp/book_search_results.html', {'form' : form, 'results' : results, 'field_data' : field_data, 
                                                                  'search_query' : search_query, 'query_string' : query_string})
    
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


#music関連（一覧、詳細、削除、検索）
def music_list(request):
    musics = Music.objects.all().order_by("singger")
    paginator = Paginator(musics, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'myapp/music_list.html', {'page_obj' : page_obj})
    

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

        results = Music.objects.filter(query).distinct().order_by('singger')
        paginator = Paginator(results, 30)
        page_number = request.GET.get('page')
        results = paginator.get_page(page_number)
        
        current_query = request.GET.copy()
        if 'page' in current_query:
            current_query.pop('page')
            current_query.pop('page')
        query_string = current_query.urlencode()
        
        for field in form:
            field_data.append({
                'field' : field,
                'is_checkbox' : isinstance(field.field.widget, forms.CheckboxSelectMultiple)
            })
        
        return render(request, 'myapp/music_search_results.html', 
                      {'form' : form, 'results' : results, 'field_data' : field_data, 'search_query' : search_query, 'query_string' : query_string})
    
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