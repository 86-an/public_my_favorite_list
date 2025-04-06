from django import forms 
from .models import Anime, Cast, Staff, Book, BookType, BookGenre, BookStatus, Value 

class BookForm(forms.ModelForm):
    types = forms.MultipleChoiceField(queryset=BookType.objects.all(),
                                      widget=forms.CheckboxSelectMultiple(), label='分類'
                                      )
    genres = forms.MultipleChoiceField(queryset=BookGenre.objects.all(),
                                       widget=forms.CheckboxSelectMultiple(), label='ジャンル'
                                       )
    statuses = forms.MultipleChoiceField(queryset=BookStatus.objects.all(),
                                         widget=forms.CheckboxSelectMultiple(), label='状態'
                                         )
    values = forms.MultipleChoiceField(queryset=Value.objects.all(),
                                       widget=forms.CheckboxSelectMultiple(), label='評価'
                                       )
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'designer', 'types', 'genres', 'series', 'statuses', 'values']