from django import forms
from .models import SongComment, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class AddTrackForm(forms.Form):
    song_name = forms.CharField(label='Название')
    artist = forms.CharField(label='Исполнитель')
    album = forms.CharField(label='Альбом', required=False)
    genre = forms.CharField(label='Жанр')
    year = forms.DateField(label='Год')
    file = forms.FileField(label='Файл')
    album_pic = forms.ImageField(label='Картинка альбома', required=False)

class Comment(forms.ModelForm):
    class Meta:
        model = SongComment
        fields = ['comment']



class UserCreate(UserCreationForm):
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')
    email = forms.EmailField()
    username = forms.CharField(label='Ник')


    class Meta:
        model = User
        fields = ['username', 'first_name','last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(UserCreate, self).save(commit = False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('location', 'avatar', 'birth_date')