from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Anime, Cast, Staff
from .resource import AnimeResource

@admin.register(Anime)
class AnimeAdmin(ImportExportModelAdmin):
    resource_class = AnimeResource
    list_display = ('title', 'media', 'episodes_count', 'season_year', 'season_name')
    search_fields = ('title', 'title_kana')

@admin.register(Cast)
class CastAdmin(admin.ModelAdmin):
    list_display = ('name', 'anime')
    search_fields = ('name',)

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('name', 'roletext', 'anime')
    search_fields = ('name', 'roletext')