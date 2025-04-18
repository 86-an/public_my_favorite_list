from django import forms
from .models import Anime, AnimeGenre, AnimeStatus, Cast, Book, BookType, BookGenre, BookStatus, Value, Music, MusicStatus

#anime検索フォーム
class AnimeSearchForm(forms.ModelForm):
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
        fields = ['title', 'title_kana', 'media', 'season_year', 'season_name', 'genres', 'statuses', 'values']
        widgets = {
            'title' : forms.TextInput(attrs = {'class' : 'form-control',
                                               'placeholder' : 'タイトルを入力してください'}),
            'title_kana' : forms.TextInput(attrs = {'class' : 'form-control',
                                               'placeholder' : 'タイトルカナを入力してください'}),
            'media' : forms.TextInput(attrs = {'class' : 'form-control',
                                               'placeholder' : 'メディアを入力してください'}),
            'season_year' : forms.NumberInput(attrs = {'class' : 'form-control',
                                               'placeholder' : '放送年度を入力してください'}),
            'season_name' : forms.TextInput(attrs = {'class' : 'form-control',
                                               'placeholder' : '季節を入力してください'}),
        }
        labels = {
            'media' : 'メディア　TV MOVIE OVA WEB OTHER ',
            'season_year' : '放送年度を半角で',
            'season_name' : '季節を全角で　SPRING SUMMER AUTUMN WINTER',
        }
    
    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
    
        if self.instance and self.instance.pk:
            self.fields['genres'].initial = self.instance.genre.all()
            self.fields['statuses'].initial = self.instance.status.all()
            self.fields['values'].initial = self.instance.value.all()


class CastSearchForm(forms.ModelForm):    
    class Meta:
        model = Cast
        fields = ['name']
        widgets = {
            'name' : forms.TextInput(attrs = {'class' : 'form-control',
                                               'placeholder' : '声優名を入力してください'}),
        }
        
    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        
        
class StaffSearchForm(forms.ModelForm):
    staff_name = forms.CharField(
        max_length=200,
        required=False,
        label="スタッフ名",
        widget=forms.TextInput(attrs={'placeholder': 'スタッフ名を入力'})
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


#musicフォーム
class MusicForm(forms.ModelForm):
    status = forms.ModelMultipleChoiceField(
        queryset = MusicStatus.objects.all(),
        widget = forms.CheckboxSelectMultiple(attrs = {'class' : 'form-check-input'}),
        label = '状態',
        required = False
    )
    
    values = forms.ModelMultipleChoiceField(
        queryset = Value.objects.all(),
        widget = forms.CheckboxSelectMultiple(attrs={'class' : 'form-check=input'}),
        label='評価',
        required = False
    )
    
    class Meta:
        model = Music
        fields = ['song_name', 'singger', 'writer','sing_writer', 'editor', 'song_write']
        widgets = {
            'song_name' : forms.TextInput(attrs={'class' : 'form-control',
                                                 'placeholder' : '曲名を入力して下さい'}),
            'singger' : forms.TextInput(attrs={'class' : 'form-control',
                                               'placeholder' : '歌手名を入力してください'}),
            'writer' : forms.TextInput(attrs={'class' : 'form-control',
                                              'placeholder' : '作曲家名を入力してください'}),
            'sing_writer' : forms.TextInput(attrs={'class' : 'form-control',
                                                   'placeholder' : '作詞家名を入力してください'}),
            'editor' : forms.TextInput(attrs={'class' : 'form-control',
                                              'placeholder' : '編曲者名を入力してください'}),
            'song_write' : forms.TextInput(attrs={'class' : 'form-control',
                                                  'placeholder' : '歌詞を入力してください' }),
        }
    
    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        
        if self.instance and self.instance.pk:
            self.fields['status'].initial = self.instance.status.all()
            self.fields['values'].initial = self.instance.value.all()