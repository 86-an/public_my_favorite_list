from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """辞書から動的にキーを取得"""
    return dictionary.get(key, None)