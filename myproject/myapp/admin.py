from django.contrib import admin
from import_export.admin import ImportExportModelAdmin, ExportMixin
from .models import Anime, Cast, Staff, BookType, BookGenre, BookStatus, Value, Book, MusicStatus, Music
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
    list_display = ('anime_title', 'name')  # アニメタイトルとキャスト名を表示
    search_fields = ('anime__title', 'name')  # アニメタイトルとキャスト名で検索可能
    list_filter = ('anime__title',)  # アニメタイトルでフィルタリング
    ordering = ('anime__title', 'name')  # アニメタイトルとキャスト名で並び替え

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('anime')  # ForeignKeyでの関連取得を効率化

    def anime_title(self, obj):
        return obj.anime.title if obj.anime else "不明なアニメ"
    anime_title.short_description = 'アニメタイトル'
    
@admin.register(Staff)
class StaffAdmin(ImportExportModelAdmin):
    resource_class = StaffResource
    list_display = ('anime_id', 'name', 'roletext')
    search_fields = ('anime_id', 'name', 'roletext')
    
    
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

#音楽関連
@admin.register(MusicStatus)
class MusicStatusAdmin(admin.ModelAdmin):
    list_display = ['name']
    
@admin.register(Music)
class MusicAdmin(ImportExportModelAdmin):
    resource_class = MusicResource
    # 管理画面で表示するフィールド
    list_display = ['song_name', 'singger', 'writer', 'sing_writer', 'editor', 'song_write', 'music_statuses', 'music_values']

    def music_statuses(self, obj):
        # 状態（ManyToManyField）のリストをカンマ区切りで表示
        return ", ".join([status.name for status in obj.status.all()])  
    music_statuses.short_description = '状態'

    def music_values(self, obj):
        # 評価（ManyToManyField）のリストをカンマ区切りで表示
        return ", ".join([value.name for value in obj.value.all()])  
    music_values.short_description = '評価'