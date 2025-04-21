from django.db import models

#評価(全クラス共通)モデル
class Value(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name='評価')
    
    def __str__(self):
        return self.name

#アニメの中間テーブル(form用)    
class AnimeGenre(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name='分類')
    
    def __str__(self):
        return self.name
    

class AnimeStatus(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name='状態')
    
    def __str__(self):
        return self.name
    
# アニメモデル
class Anime(models.Model):
    anime_id = models.CharField(max_length=200, unique=True, verbose_name='アニメID')
    title = models.CharField(max_length=200, blank=True, null=True, verbose_name='タイトル')
    title_kana = models.CharField(max_length=200, blank=True, null=True, verbose_name='タイトルカナ')  # 空データを許容
    media = models.CharField(max_length=200, blank=True, null=True, verbose_name='メディア')
    episodes_count = models.IntegerField(verbose_name='話数', default=0)  # デフォルト値で空を防ぐ
    season_year = models.IntegerField(verbose_name='年', blank=True, null=True, )  # デフォルト値で整合性維持
    season_name = models.CharField(max_length=200, blank=True, null=True, verbose_name='季節')
    comment = models.CharField(max_length=300, blank=True, null=True, verbose_name='コメント') # 空データを許容
    genre = models.ManyToManyField(AnimeGenre, verbose_name='ジャンル', blank=True, related_name='animes_genre')
    status = models.ManyToManyField(AnimeStatus, verbose_name='状態', blank=True, related_name='animes_status')
    value = models.ManyToManyField(Value, verbose_name='評価', blank=True, related_name='animes_value')
    
    def __str__(self):
        return self.title if self.title else "不明なアニメ"
    
    
# キャストモデル リレーション多対多
class Cast(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE,
                                 related_name='casts', verbose_name="アニメ")
    name = models.CharField(max_length=200, blank=True, null=True, verbose_name='声優名')  # 空のデータを許容

    def __str__(self):
        return self.name if self.name else "不明なキャスト"

# スタッフモデル　
class Staff(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, null=True,
                                 related_name='staff', verbose_name="アニメ")
    staff_id = models.CharField(max_length=200, blank=True, null=True, verbose_name='スタッフID')  # 空のデータを許容
    name = models.CharField(max_length=200, blank=True, null=True, verbose_name='スタッフ名')  # 空のデータを許容
    roletext = models.CharField(max_length=200, blank=True, null=True, verbose_name='役割')  # 空データを許容

    def __str__(self):
        return f"{self.name} ({self.roletext})" if self.name else "不明なスタッフ"


#book中間テーブル(form用)
class BookType(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name='分類')
    
    def __str__(self):
        return self.name


class BookGenre(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name='ジャンル')
    
    def __str__(self):
        return self.name


class BookStatus(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name='状態')
    
    def __str__(self):
        return self.name
    


    
#bookモデル    
class Book(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True, verbose_name='タイトル')
    author = models.CharField(max_length=200, blank=True, null=True, verbose_name='著者')
    designer = models.CharField(max_length=200, blank=True, null=True, verbose_name='絵師')
    type = models.ManyToManyField(BookType, verbose_name='分類', blank=True, related_name='books_type')
    genre = models.ManyToManyField(BookGenre, verbose_name='ジャンル', blank=True, related_name='books_genre')
    series = models.IntegerField(verbose_name='巻数', default=1)
    status = models.ManyToManyField(BookStatus, verbose_name='状態', related_name='books_status')
    value = models.ManyToManyField(Value, verbose_name='評価', blank=True, related_name='books_value')


#音楽の中間モデル
class MusicStatus(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name='状態')
    def __str__(self):
        return self.name

#音楽モデル
class Music(models.Model):
    song_name = models.CharField(max_length=200, blank=True, null=True, verbose_name='曲名')
    singger = models.CharField(max_length=200, blank=True, null=True, verbose_name='歌手')
    writer = models.CharField(max_length=200, blank=True, null=True, verbose_name='作曲者')
    sing_writer = models.CharField(max_length=200, blank=True, null=True, verbose_name='作詞家')
    editor = models.CharField(max_length=200, blank=True, null=True, verbose_name='編曲者')
    song_write = models.CharField(max_length=2000, blank=True, null=True, verbose_name='歌詞')
    status = models.ManyToManyField(MusicStatus, verbose_name='状態', blank=True, related_name='music_status')
    value = models.ManyToManyField(Value, verbose_name='評価', blank=True, related_name='music_value')

