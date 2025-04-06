from django import forms
from .models import Anime, Cast, Staff, Book, BookType, BookGenre, BookStatus, Value

class BookForm(forms.ModelForm):
    # 分類のチェックボックス
    types = forms.ModelMultipleChoiceField(
        queryset=BookType.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        label='分類'  # タイトル「分類」に変更
    )
    # ジャンルのチェックボックス
    genres = forms.ModelMultipleChoiceField(
        queryset=BookGenre.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        label='ジャンル'  # 修正: 本来のタイトルへ
    )
    # 状態のチェックボックス
    statuses = forms.ModelMultipleChoiceField(
        queryset=BookStatus.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        label='状態'  # 修正: 本来のタイトルへ
    )
    # 評価のチェックボックス
    values = forms.ModelMultipleChoiceField(
        queryset=Value.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        label='評価'  # 修正: 本来のタイトルへ
    )

    class Meta:
        model = Book
        fields = ['title', 'author', 'designer', 'types', 'genres', 'series', 'statuses', 'values']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'タイトルを入力してください'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '著者名を入力してください'}),
            'designer': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '絵師を入力してください'}),
            'series': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '巻数を入力してください'}),
        }