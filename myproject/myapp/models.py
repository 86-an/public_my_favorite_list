from django.db import models

# モデルを定義
class Anime(models.Model):
    anime_id = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    title_kana = models.CharField(max_length=200)
    media = models.CharField(max_length=200)
    episodes_count = models.IntegerField()  # max_lengthを削除しました
    season_year = models.IntegerField()
    season_name = models.CharField(max_length=200)
    # ジャンル、評価、視聴済みフラグなどを追加する場合の例:
    # genre = models.CharField(max_length=200)
    # rating = models.FloatField()
    # watched = models.BooleanField()

class Cast(models.Model):
    cast_id = models.CharField(max_length=200, blank=True, null=True)  # 空のデータを許容
    name = models.CharField(max_length=200, blank=True, null=True)  # 空のデータを許容
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='cast')
    
class Staff(models.Model):
    staff_id = models.CharField(max_length=200, blank=True, null=True)  # 空のデータを許容
    name = models.CharField(max_length=200, blank=True, null=True)  # 空のデータを許容
    roletext = models.CharField(max_length=200, blank=True, null=True)  # 空のデータを許容
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='staff')