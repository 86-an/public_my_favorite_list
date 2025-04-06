from django.db import models

# アニメモデル
class Anime(models.Model):
    anime_id = models.CharField(max_length=200, unique=True, verbose_name='アニメID')
    title = models.CharField(max_length=200, verbose_name='タイトル')
    title_kana = models.CharField(max_length=200, blank=True, null=True, verbose_name='タイトルカナ')  # 空データを許容
    media = models.CharField(max_length=200, verbose_name='メディア')
    episodes_count = models.IntegerField(verbose_name='話数', default=0)  # デフォルト値で空を防ぐ
    season_year = models.IntegerField(verbose_name='年', default=0)  # デフォルト値で整合性維持
    season_name = models.CharField(max_length=200, blank=True, null=True, verbose_name='季節')  # 空データを許容

    def __str__(self):
        return self.title

# キャストモデル リレーション多対多
class Cast(models.Model):
    anime_id = models.CharField(max_length=200, unique=True, verbose_name='アニメID', null=True)
    name = models.CharField(max_length=200, blank=True, null=True, verbose_name='声優名')  # 空のデータを許容
    animes = models.ManyToManyField('Anime', related_name='casts')  # 多対多リレーション

    def __str__(self):
        return self.name if self.name else "不明なキャスト"

# スタッフモデル　リレーション
class Staff(models.Model):
    anime_staff_id = models.CharField(max_length=200, default='unknown')
    staff_id = models.CharField(max_length=200, blank=True, null=True, verbose_name='スタッフID')  # 空のデータを許容
    name = models.CharField(max_length=200, blank=True, null=True, verbose_name='スタッフ名')  # 空のデータを許容
    roletext = models.CharField(max_length=200, blank=True, null=True, verbose_name='役割')  # 空データを許容
    anime_id = models.ForeignKey(Anime, to_field='anime_id', on_delete=models.CASCADE, related_name='staff')

    def __str__(self):
        return f"{self.name} ({self.roletext})" if self.name else "不明なスタッフ"


#book中間テーブル
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
    

class Value(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name='評価')
    
    def __str__(self):
        return self.name
    
#bookモデル    
class Book(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True, verbose_name='タイトル')
    author = models.CharField(max_length=200, blank=True, null=True, verbose_name='著者')
    designer = models.CharField(max_length=200, blank=True, null=True, verbose_name='絵師')
    type = models.ManyToManyField(BookType, verbose_name='分類')
    genre = models.ManyToManyField(BookGenre, verbose_name='ジャンル')
    series = models.IntegerField(verbose_name='巻数', default=1)
    status = models.ManyToManyField(BookStatus, verbose_name='状態')
    value = models.ManyToManyField(Value, verbose_name='評価')


