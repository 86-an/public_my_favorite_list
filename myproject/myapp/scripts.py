from myapp.models import Anime, AnimeGenre, AnimeStatus, BookType, BookGenre, BookStatus, Value

# Valueのデータ登録
for name in ['SS', 'S', 'A', 'B', 'C', 'D']:
    Value.objects.get_or_create(name=name)
    
#AnimeGenreのデータ登録
for name in ['SF/ファンタジー', 'ロボット/メカ', 'アクション/バトル', 
             'コメディ/ギャグ', '恋愛/ラブコメ', '日常/ほのぼの','スポーツ/競技', 'ホラー', 'サスペンス/推理', 
             '歴史/戦記', '戦争/ミリタリー', 'ドラマ/青春', 'キッズ/ファミリー', 'ショート']:
    AnimeGenre.objects.get_or_create(name=name)

#AnimeStatusのデータ登録
for name in ['未視聴', '視聴中', '視聴済み', '気になる']:
    AnimeStatus.objects.get_or_create(name=name)

#AnimeSearchFormのデータ登録
MEDIA_CHOICES = [
    ('TV', 'TV'),
    ('OVA', 'OVA'),
    ('MOVIE', 'MOVIE'),
    ('WEB', 'WEB'),
    ('OTHER', 'OTHER'),
]

SEASON_NAME_CHOICES = [
    ('SPRING', '春'),
    ('SUMMER', '夏'),
    ('AUTUMN', '秋'),
    ('WINTER', '冬'),
]

SEASON_YEAR_CHOICES = [
    (year['season_year'], year['season_year'])
    for year in Anime.objects.values('season_year').distinct()
]

# BookTypeのデータ登録
for name in ['小説', 'ライトノベル', '漫画', 'ビジネス本', 'お金']:
    BookType.objects.get_or_create(name=name)

# BookGenreのデータ登録
for name in ['推理・ミステリー', '青春', '恋愛', 'SF(サイエンスフィクション)', 'ファンタジー',
             'ホラー', '経済', '政治', '歴史・時代', 'ミリタリー', '児童', '官能']:
    BookGenre.objects.get_or_create(name=name)

# BookStatusのデータ登録
for name in ['未読', '読書中', '読了', '購入済み', '気になる']:
    BookStatus.objects.get_or_create(name=name)
