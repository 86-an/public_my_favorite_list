from import_export import resources, fields
from .models import Anime, Cast, Staff
import logging

logger = logging.getLogger(__name__)

class AnimeResource(resources.ModelResource):
    anime_id = fields.Field(attribute='anime_id', column_name='id')  # JSONの"id"をanime_idにマッピング
    title = fields.Field(attribute='title', column_name='title')
    title_kana = fields.Field(attribute='title_kana', column_name='titleKana')
    media = fields.Field(attribute='media', column_name='media')
    episodes_count = fields.Field(attribute='episodes_count', column_name='episodesCount')
    season_year = fields.Field(attribute='season_year', column_name='seasonYear')
    season_name = fields.Field(attribute='season_name', column_name='seasonName')

    class Meta:
        model = Anime
        fields = ('anime_id', 'title', 'title_kana', 'media', 'episodes_count', 'season_year', 'season_name')
        import_id_fields = ('anime_id',)  # 一意識別子としてanime_idを指定


class CastResource(resources.ModelResource):
    anime_id = fields.Field(attribute='anime_id', column_name='anime_id')  # カラム名指定
    name = fields.Field(attribute='name', column_name='name')
    
    def before_import_row(self, row, **kwargs):
        if 'import_type' in row:
            del row['import_type']
            logger.info("Removed 'import_type' from row.")
        try:
            row['anime_id'] = Anime.objects.get(anime_id=row['anime_id']).anime_id
        except Anime.DoesNotExist:
            raise ValueError(f"Anime with anime_id '{row['anime_id']}' does not exist.")
            
    class Meta:
        model = Cast
        fields = ('anime_id', 'name')  # 'id'は含めない
        import_id_fields = ('anime_id', )  # anime_cast_idを照合基準に


class StaffResource(resources.ModelResource):
    anime_staff_id = fields.Field(attribute='anime_staff_id', column_name='anime_staff_id')
    staff_id = fields.Field(attribute='staff_id', column_name='id')
    name = fields.Field(attribute='name', column_name='name')
    roletext = fields.Field(attribute='roletext', column_name='roleText')
    anime_id = fields.Field(attribute='anime_id', column_name='anime_id')
    
    def before_import_row(self, row, **kwargs):
        if 'import_type' in row:
            del row['import_type']
            logger.info("Removed 'import_type' from row.")
        try:
            row['anime_id'] = Anime.objects.get(anime_id=row['anime_id'])
        except Anime.DoesNotExist:
            raise ValueError(f"Anime with anime_id '{row['anime_id']}' does not exist.")
        
    class Meta:
        model = Staff
        fields = ('anime_staff_id', 'anime_id', 'staff_id', 'name', 'roletext')
        import_id_fields = ('anime_staff_id',)  
