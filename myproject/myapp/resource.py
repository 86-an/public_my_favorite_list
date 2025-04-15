from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import Anime, Cast, Staff, Music
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
    anime_id = fields.Field(
        column_name='anime_id',
        attribute='anime',
        widget=ForeignKeyWidget(Anime, 'anime_id')
    )
    name = fields.Field(attribute='name', column_name='name')

    def before_import_row(self, row, **kwargs):
        try:
            anime = Anime.objects.get(anime_id=row['anime_id'])
            row['anime'] = anime
        except Anime.DoesNotExist:
            logger.warning(f"Anime with anime_id '{row['anime_id']}' does not exist. Skipping row.")
            row['anime'] = None

        # 既存データチェックで上書きを回避
        if Cast.objects.filter(anime__anime_id=row['anime_id'], name=row['name']).exists():
            logger.info(f"Cast '{row['name']}' for anime '{row['anime_id']}' already exists. Skipping row.")
            return None  # スキップ行として処理

    class Meta:
        model = Cast
        fields = ('anime_id', 'name')
        import_id_fields = ('anime_id', 'name')  # anime_idとnameの組み合わせを基準に識別


class StaffResource(resources.ModelResource):
    anime = fields.Field(
        column_name='anime_id',attribute='anime',
        widget=ForeignKeyWidget(Anime, 'anime_id')  # Animeモデルのanime_idを参照
    )
    staff_id = fields.Field(attribute='staff_id', column_name='staff_id')
    name = fields.Field(attribute='name', column_name='name')
    roletext = fields.Field(attribute='roletext', column_name='roleText')
        
    class Meta:
        model = Staff
        fields = ('anime_id', 'staff_id', 'name', 'roletext')
        import_id_fields = ('anime_id',)  


class MusicResource(resources.ModelResource):
    song_name = fields.Field(attribute='song_name', column_name='曲名')
    singger = fields.Field(attribute='singger', column_name='歌手名')
    writer = fields.Field(attribute='writer', column_name='作詞者名')
    sing_writer = fields.Field(attribute='sing_writer', column_name='作曲者名')
    editor = fields.Field(attribute='editor', column_name='編曲者名')
    song_write = fields.Field(attribute='song_write', column_name='歌い出し')
    
    class Meta:
        model = Music
        fields = ('song_name', 'singger', 'writer', 'sing_writer', 'editor', 'song_write')
        import_id_fields = ('song_name',)
    
    
