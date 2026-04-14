from django import forms
from .models import Post, Category

class PostForm(forms.ModelForm):
    category_name = forms.CharField(required=False)

    class Meta:
        model = Post
        fields = ['title', 'content']   

    def save(self, commit=True):
        post = super().save(commit=False)

        category_name = self.cleaned_data.get('category_name')

        if category_name:
            category, created = Category.objects.get_or_create(name=category_name)
            post.category = category

        if commit:
            post.save()

        return post