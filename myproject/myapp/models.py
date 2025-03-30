from django.db import models

# モデルを定義
class Anime(models.Model):
    anime_id = models.CharField(max_length=200, verbose_name='アニメID')
    title = models.CharField(max_length=200, verbose_name='タイトル')
    title_kana = models.CharField(max_length=200, verbose_name='タイトルカナ')
    media = models.CharField(max_length=200, verbose_name='メディア')
    episodes_count = models.IntegerField(verbose_name='話数')  # max_lengthを削除しました
    season_year = models.IntegerField(verbose_name='年')
    season_name = models.CharField(max_length=200, verbose_name='季節')
    # ジャンル、評価、視聴済みフラグなどを追加する場合の例:
    # genre = models.CharField(max_length=200)
    # rating = models.FloatField()
    # watched = models.BooleanField()

class Cast(models.Model):
    cast_id = models.CharField(max_length=200, blank=True, null=True, verbose_name='キャストID')  # 空のデータを許容
    name = models.CharField(max_length=200, blank=True, null=True, verbose_name='声優名')  # 空のデータを許容
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='cast')
    
class Staff(models.Model):
    staff_id = models.CharField(max_length=200, blank=True, null=True, verbose_name='スタッフID')  # 空のデータを許容
    name = models.CharField(max_length=200, blank=True, null=True, verbose_name='スタッフ名')  # 空のデータを許容
    roletext = models.CharField(max_length=200, blank=True, null=True, verbose_name='役割')  # 空のデータを許容
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='staff')