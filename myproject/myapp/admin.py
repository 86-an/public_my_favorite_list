from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Anime, Cast, Staff
from .resource import AnimeResource, CastResource, StaffResource

@admin.register(Anime)
class AnimeAdmin(ImportExportModelAdmin):
    resource_class = AnimeResource
    list_display = ('title', 'media', 'episodes_count', 'season_year', 'season_name')
    search_fields = ('title', 'title_kana', 'media')

@admin.register(Cast)
class CastAdmin(ImportExportModelAdmin):
    resource_class = CastResource
    list_display = ('name', 'anime_id')
    search_fields = ('name','anime_id__title')

@admin.register(Staff)
class StaffAdmin(ImportExportModelAdmin):
    resource_class = StaffResource
    list_display = ('name', 'roletext', 'anime_id')
    search_fields = ('name', 'roletext', 'anime_id__title')