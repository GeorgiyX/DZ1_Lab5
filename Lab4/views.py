from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from Lab4 import FilesList
from django.views.generic import View
from .Forms import AddTrackForm
from .models import GetTrackList, GetTrackInfo, Connection, Tracks_cls, Save_file
#Для пользователей:
from django.views.generic.edit import FormView
from .Forms import UserCreate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import  login, logout

def index(request):
    dict = FilesList.Get2ListOfFile()
    return render(request, 'index_final.html', context=dict)
def resp(request, param):
    return HttpResponse("You say:" + param)
def AboutTrack(request, name):
    diction = {'val' : name}
    diction['info'] = FilesList.Mp3Info(diction['val'])
    return render(request, 'AboutTrack.html', context=diction)
def redir(request):
    return HttpResponseRedirect("/ ")


#CBV
class IndexPage(View):
    '''CBV для главной страницы с формой'''

    def get(self, request):
        if request.user.is_authenticated:
            form = AddTrackForm()
            dict = {'form' : form, 'songs' : GetTrackList()}
            return render(request, 'index_final.html', context=dict)
        else:
            return HttpResponseRedirect('/login')

    def post(self, request):
        form = AddTrackForm(request.POST, request.FILES)
        print('\n\n\n\n Im in\n viev! \n\n\n\n')
        dict = {'form' : form, 'songs' : GetTrackList()} #для озврата формы в случае не валида
        if form.is_valid():
            print('\n\n\n\n Form valid! \n\n\n\n')
            self.con = Connection()
            self.song_name = form.cleaned_data["song_name"]
            self.artist = form.cleaned_data["artist"]
            self.album = form.cleaned_data["album"]
            self.genre = form.cleaned_data["genre"]
            self.year = form.cleaned_data["year"]
            self.file_name = str('Saved_Media/'+self.song_name + ' - ' + self.artist+".mp3")
            Save_file(request.FILES['file'],self.file_name)
            self.pic_name = 'Saved_Media/Default.png'
            if 'album_pic' in request.FILES:
                self.pic_name = str('Saved_Media/' + self.song_name  + ' - ' +  self.artist + ".jpg")
                Save_file(request.FILES['album_pic'], self.pic_name)
            self.redirect_adress =str('music/' + self.artist + '/' + self.song_name)
            with self.con:
                track = Tracks_cls(self.con)
                track.save(self.song_name,self.artist,self.genre,self.year,self.file_name,album=self.album, album_pic=self.pic_name)
            return HttpResponseRedirect(self.redirect_adress)
        else:
            print('\n\n\n\n Im NOT VALID! BB \n\n\n\n')
            return render(request, 'index_final.html', context=dict)

class TrackPage(View):
    '''CBV для страницы с сущностью'''

    def get(self, request,artist, song ):
        if request.user.is_authenticated:
            dict = {'info' : GetTrackInfo(song, artist)}
            return render(request, 'TrackPage.html', context=dict)
        else:
            return HttpResponseRedirect('/login')

    # def post(self, request):
    #     form =
    #     dict = {'form' : form, } #для озврата формы в случае не валида
    #     if form.is_valid():
    #         return HttpResponseRedirect('')
    #     return render(request, '', context=dict)


#===Регистрация, Логин, Логаут===

class Registration(FormView):
    form_class = UserCreate
    success_url = '/login'
    template_name ='Registration.html'

    def form_valid(self, form):
        form.save()
        return super(Registration, self).form_valid(form)
    def form_invalid(self, form):
        return super(Registration, self).form_invalid(form)


class LogIn(FormView):
    form_class = AuthenticationForm
    success_url = '/'
    template_name = 'LogIn.html'

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LogIn, self).form_valid(form)

class LogOut(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')
