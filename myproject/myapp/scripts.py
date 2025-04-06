from myapp.models import BookType, BookGenre, BookStatus, Value

# Valueのデータ登録
for name in ['SS', 'S', 'A', 'B', 'C', 'D']:
    Value.objects.get_or_create(name=name)

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