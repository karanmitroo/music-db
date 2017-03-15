from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate, login
from django.views.generic import View
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Album, Song
from .forms import UserForm
from .serializers import AlbumSerializer, SongSerializer

class IndexView(generic.ListView):
	template_name = "music/index.html"
	context_object_name = 'all_albums'

	def get_queryset(self):
		return Album.objects.all()


class SongsView(generic.ListView):
	template_name = "music/all_songs.html"
	context_object_name = 'all_songs'

	def get_queryset(self):
		return Song.objects.all()


class DetailView(generic.DetailView):
	model = Album
	template_name = "music/detail.html"

class AlbumCreate(CreateView):
	model = Album
	fields = ['artist', 'album_title', 'genre', 'album_logo']

class AlbumUpdate(UpdateView):
	model = Album
	fields = ['artist', 'album_title', 'genre', 'album_logo']


class AlbumDelete(DeleteView):
	model = Album
	success_url = reverse_lazy('music:index')

def album_favorite(request, album_id):
	album = Album.objects.get(pk = album_id)
	if album.is_favorite:
		album.is_favorite = False
	else:
		album.is_favorite = True
	album.save()
	context = {
	'all_albums' : Album.objects.all()
	}
	return render(request, "music/index.html", context)

def song_favorite(request, song_id):
	song = Song.objects.get(pk = song_id)
	if song.is_favorite:
		song.is_favorite = False
	else:
		song.is_favorite = True
	song.save()
	context = {
	'all_albums' : Album.objects.all()
	}
	return render(request, "music/detail.html", context)


class UserFormView(View):
	form_class = UserForm
	template_name = 'music/registration_form.html'

	#Display blank form
	def get(self, request):
		form = self.form_class(None)
		return render(request, self.template_name, {'form' : form})

	#Process form data to add user to db
	def post(self, request):
		form = self.form_class(request.POST)

		if form.is_valid():

			user = form.save(commit=False)

			#Cleaned(Normalised) Data
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user.set_password(password)
			user.save()

			#return user objects if credentials are correct
			user = authenticate(username = username, password = password)

			if user is not None:
				if user.is_active:

					login(request, user)
					return redirect("music:index")

		return render(request, self.template_name, {'form' : form})


#/albums/api
class AlbumList(APIView):

	def get(self, request):
		albums = Album.objects.all()
		serializer = AlbumSerializer(albums, many=True)
		return Response(serializer.data)


class SongList(APIView):

	def get(self, request):
		songs = Song.objects.all()
		serializer = SongSerializer(songs, many=True)
		return Response(serializer.data)

#/song/api

# class FavoriteUpdate(generic.ListView):
#
# 	def get_object(self, **kwargs):
# 		object = super(FavoriteUpdate, **kwargs),get_object()
# 		object.is_favorite = True
# 		object.save()
#
# 	template_name = "music/index.html"
# 	context_object_name = 'all_albums'
#
# 	def get_queryset(self):
# 		return Album.objects.all()
