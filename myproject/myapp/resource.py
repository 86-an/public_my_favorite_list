from import_export import resources, fields
from .models import Anime, Cast, Staff
import logging

logger = logging.getLogger(__name__)

class AnimeResource(resources.ModelResource):
    anime_id = fields.Field(attribute='anime_id')
    title = fields.Field(attribute='title')
    title_kane = fields.Field(attribute='title_kana')
    media = fields.Field(attribute='media')
    episodes_count = fields.Field(attribute='episodes_count')
    season_year = fields.Field(attribute='season_year')
    season_name = fields.Field(attribute='season_name')
    
    class Meta:
        model = Anime
        fields = ('anime_id', 'title', 'title_kana', 'media', 'episodes_count', 'season_year', 'season_name')

    def before_import_row(self, row, **kwargs):
        # `import_type`フィールドを削除してエラーを回避
        if 'import_type' in row:
            del row['import_type']
            logger.info("Removed 'import_type' from row")

class CastResource(resources.ModelResource):
    cast_id = fields.Field(attribute='cast_id')
    name = fields.Field(attribute='name')
    anime = fields.Field(attribute='anime')
    
    class Meta:
        model = Cast
        fields = ('cast_id', 'name', 'anime')  # `anime`はForeignKey

class StaffResource(resources.ModelResource):
    staff_id = fields.Field(attribute='staff_id')
    name = fields.Field(attribute='name')
    roletext = fields.Field(attribute='roletext')
    anime = fields.Field(attribute='anime')
    
    class Meta:
        model = Staff
        fields = ('staff_id', 'name', 'roletext', 'anime')  # `anime`はForeignKey