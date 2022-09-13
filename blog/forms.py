from django import forms

from ckeditor.fields import RichTextField

from .models import Category, Post


class PostForm(forms.ModelForm):
    class Meta:
        choices = Category.objects.all().values_list('name', 'name')
        choices_list = list()
        for item in choices:
            choices_list.append(item)
        model = Post
        fields = ['author', 'category', 'title', 'content', 'snippet', 'image', 'slug']
        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Iltimos post mavzusini kiriting!!!'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'id': 'author', 'type': 'hidden'}),
            'category': forms.Select(choices=choices_list, attrs={'class': 'form-control'}),
            'content': RichTextField(),
            'snippet': forms.Textarea(attrs={'class': 'form-control'}),
        }


class EditPostForm(forms.ModelForm):
    class Meta:
        choices = Category.objects.all().values_list('name', 'name')
        choices_list = list()
        for item in choices:
            choices_list.append(item)
        model = Post
        fields = ['category', 'title', 'content', 'snippet', 'image', 'slug']
        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Iltimos post mavzusini kiriting!!!'}),
            'snippet': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(choices=choices_list, attrs={'class': 'form-control'}),
            'content': RichTextField(),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Iltimos yangi toifa nomini kiriting!!!'})
        }
