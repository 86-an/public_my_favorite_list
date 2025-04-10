from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Anime, Cast, Staff, BookType, BookGenre, BookStatus, Value, Book, Music
from .resource import AnimeResource, CastResource, StaffResource, MusicResource

#anime関連
@admin.register(Anime)
class AnimeAdmin(ImportExportModelAdmin):
    resource_class = AnimeResource
    list_display = ('title', 'media', 'episodes_count', 'season_year', 'season_name')
    search_fields = ('title', 'title_kana', 'media')

@admin.register(Cast)
class CastAdmin(ImportExportModelAdmin):
    resource_class = CastResource
    list_display = ('name', 'get_animes')  # 多対多リレーション用のカスタムメソッド
    search_fields = ('name', 'animes__title')  # 多対多リレーションのタイトルで検索可能

    def get_animes(self, obj):
        return ", ".join([anime.title for anime in obj.animes.all()])
    get_animes.short_description = 'Animes'

@admin.register(Staff)
class StaffAdmin(ImportExportModelAdmin):
    resource_class = StaffResource
    list_display = ('name', 'roletext', 'anime_id')
    search_fields = ('name', 'roletext', 'anime_id__title')


#book関連
@admin.register(BookType)
class BookTypeAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(BookGenre)
class BookGenreAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(BookStatus)
class BookStatusAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Value)
class ValueAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'series', 'display_genres', 'display_types', 'display_statuses']
    filter_horizontal = ['type', 'genre', 'status', 'value']

    def display_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genre.all()])
    display_genres.short_description = 'ジャンル'

    def display_types(self, obj):
        return ", ".join([book_type.name for book_type in obj.type.all()])
    display_types.short_description = '分類'

    def display_statuses(self, obj):
        return ", ".join([status.name for status in obj.status.all()])
    display_statuses.short_description = '状態'

@admin.register(Music)
class MusicAdmin(ImportExportModelAdmin):
    resource_class = MusicResource
    list_display = ['song_name', 'singger', 'writer', 'sing_writer', 'editor', 'song_write']
    
