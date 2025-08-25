from django import forms
from .models import Post, Comment

class PostCreateForm(forms.ModelForm):
    """
    Форма добавления статей на сайте
    """
    class Meta:
        model = Post
        fields = ('title', 'slug', 'category', 'description', 'text', 'thumbnail', 'status')
        
    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы под Bootstrap
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })
            
            
class PostUpdateForm(PostCreateForm):
    """
    Форма обновления статьи на сайте
    """
    class Meta:
        model = Post
        fields = PostCreateForm.Meta.fields + ('updater', 'fixed')
        
    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы под Bootstrap
        """
        super().__init__(*args, **kwargs)
        
        self.fields['fixed'].widget.attrs.update({
            'class': 'form-check-input'
        })        
        
    
class CommentCreateForm(forms.ModelForm):
    """
    Форма добавления комментариев к статьям
    """
    parrent = forms.IntegerField(widget=forms.HiddenInput, required=False)
    content = forms.CharField(label='', widget=forms.Textarea(attrs={
        'class': 'form-control', 'rows': 5, 'cols': 30, 'placeholder': 'Комментарий'
    }))
    
    class Meta:
        model = Comment
        fields = ('content', )