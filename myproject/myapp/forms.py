from django import forms
from .models import Anime, AnimeGenre, AnimeStatus, Cast, Staff, Book, BookType, BookGenre, BookStatus, Value
from .scripts import MEDIA_CHOICES, SEASON_YEAR_CHOICES, SEASON_NAME_CHOICES
import logging

logger = logging.getLogger(__name__)
#anime検索フォーム
class AnimeSearchForm(forms.ModelForm):
    medias = forms.ChoiceField(
        choices=[(media, media) for media in Anime.objects.values_list("media", flat=True).distinct()],
        widget=forms.Select(attrs={"class": "form-select"}),
        label="メディア",
        required=False,
    )
    
    season_year = forms.ChoiceField(
        choices = SEASON_YEAR_CHOICES,
        widget = forms.Select(attrs = {'class' : 'form-select'}),
        label = '放送年度',
        required=False,
    )
    
    season_name = forms.ChoiceField(
        choices = SEASON_NAME_CHOICES,
        widget = forms.Select(attrs = {'class' : 'form-select'}),
        label = '季節',
        required=False,
    )
    
    genres = forms.ModelMultipleChoiceField(
        queryset = AnimeGenre.objects.all(),
        widget = forms.CheckboxSelectMultiple(attrs = {'class' : 'form-check-input'}),
        label = 'ジャンル',
        required = False,
    )
    
    statuses = forms.ModelMultipleChoiceField(
        queryset = AnimeStatus.objects.all(),
        widget = forms.CheckboxSelectMultiple(attrs = {'class' : 'form-check-input'}),
        label = '状態',
        required = False,
    )
    
    values = forms.ModelMultipleChoiceField(
        queryset = Value.objects.all(),
        widget = forms.CheckboxSelectMultiple(attrs = {'class' : 'form-check-input'}),
        label = '評価',
        required = False,
    )
    
    class Meta:
        model = Anime
        fields = ['title', 'title_kana', 'medias', 'season_year', 'season_name', 'genres', 'statuses', 'values']
        widgets = {
            'title' : forms.TextInput(attrs = {'class' : 'form-control',
                                               'placeholder' : 'タイトルを入力してください'}),
            'title_kana' : forms.TextInput(attrs = {'class' : 'form-control',
                                               'placeholder' : 'タイトルカナを入力してください'}),
        }
    
    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
    
        if self.instance and self.instance.pk:
            self.fields['medias'].initial = self.instance.media
            logger.info(f"medias: {self.fields['medias'].initial}")
            self.fields['season_year'].initial = self.instance.season_year
            self.fields['season_name'].initial = self.instance.season_name
            self.fields['genres'].initial = self.instance.genre.all()
            self.fields['statuses'].initial = self.instance.status.all()
            self.fields['values'].initial = self.instance.value.all()


class CastSearchForm(forms.Form):    
    cast_name = forms.CharField(
        required=False,
        label='声優名',
        widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : '声優名を入れてください'})
    )
        
        
class StaffSearchForm(forms.Form):
    staff_name = forms.CharField(
        required=False,
        label='スタッフ名前・役職・会社名',
        widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'スタッフ名前・役職・会社名を入れてください'})
    )

        
#animeフォーム
class AnimeForm(forms.ModelForm):
    genres = forms.ModelMultipleChoiceField(
        queryset = AnimeGenre.objects.all(),
        widget = forms.CheckboxSelectMultiple(attrs = {'class' : 'form-check-input'}),
        label = 'ジャンル',
        required = False,
    )
    
    statuses = forms.ModelMultipleChoiceField(
        queryset = AnimeStatus.objects.all(),
        widget = forms.CheckboxSelectMultiple(attrs = {'class' : 'form-check-input'}),
        label = '状態',
        required = False,
    )
    
    values = forms.ModelMultipleChoiceField(
        queryset = Value.objects.all(),
        widget = forms.CheckboxSelectMultiple(attrs = {'class' : 'form-check-input'}),
        label = '評価',
        required = False,
    )
    
    class Meta:
        model = Anime
        fields = ['genres', 'statuses', 'values']
    
    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        
        if self.instance and self.instance.pk:
            self.fields['genres'].initial = self.instance.genre.all()
            self.fields['statuses'].initial = self.instance.status.all()
            self.fields['values'].initial = self.instance.value.all()
            

#bookフォーム
class BookForm(forms.ModelForm):
    # 分類のチェックボックス
    types = forms.ModelMultipleChoiceField(
        queryset=BookType.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        label='分類',  # タイトル「分類」に変更
        required = False,
    )
    # ジャンルのチェックボックス
    genres = forms.ModelMultipleChoiceField(
        queryset=BookGenre.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        label='ジャンル',  # 修正: 本来のタイトルへ
        required=False,
    )
    # 状態のチェックボックス
    statuses = forms.ModelMultipleChoiceField(
        queryset=BookStatus.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        label='状態',  # 修正: 本来のタイトルへ
        required = False,
    )
    # 評価のチェックボックス
    values = forms.ModelMultipleChoiceField(
        queryset=Value.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        label='評価',  # 修正: 本来のタイトルへ
        required=False,
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
    
    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        
        if request and request.path == '/book/search/':
            self.fields.pop('series')
        
        if self.instance and self.instance.pk:  # 編集モードの場合
            # ManyToManyFieldの初期値を設定
            self.fields['types'].initial = self.instance.type.all()
            self.fields['genres'].initial = self.instance.genre.all()
            self.fields['statuses'].initial = self.instance.status.all()
            self.fields['values'].initial = self.instance.value.all()
