from import_export import resources
from .models import Anime, Cast, Staff
import json

class AnimeResource(resources.ModelResource):
        
    def import_row(self, row, instance_loader, **kwargs):
        # Anime情報を取得または作成
        anime_instance, created = Anime.objects.get_or_create(
            anime_id=row.get("id"),
            defaults={
                "title": row.get("title", "") or "未設定",
                "title_kana": row.get("titleKana", "") or "未設定",
                "media": row.get("media", "") or "未設定",
                "episodes_count": row.get("episodesCount", 0),
                "season_year": row.get("seasonYear", 0),
                "season_name": row.get("seasonName", "") or "未設定",
            }
        )

        # キャスト情報を登録
        casts_data = row.get("casts")
        if casts_data and "edges" in casts_data:  # 空または`edges`キーがない場合を防ぐ
            for cast in casts_data.get("edges", []):
                node = cast.get("node", {})
                Cast.objects.get_or_create(
                    anime=anime_instance,
                    name=node.get("name", "") or "未設定",  # nameがない場合も対応
                    defaults={
                        "cast_id": node.get("character", {}).get("name", "") or "未設定"  # characterが欠落していても処理可能
                    }
                )

        # スタッフ情報を登録
        staffs_data = row.get("staffs")
        if staffs_data and "edges" in staffs_data:  # 空または`edges`キーがない場合を防ぐ
            for staff in staffs_data.get("edges", []):
                node = staff.get("node", {})
                Staff.objects.get_or_create(
                    anime=anime_instance,
                    name=node.get("name", "") or "未設定",  # nameがない場合も対応
                    defaults={
                        "roletext": node.get("roleText", "") or "未設定",  # roleTextが欠落している場合に対応
                        "staff_id": node.get("id", "") or "未設定"  # idが欠落している場合に対応
                    }
                )

        return anime_instance