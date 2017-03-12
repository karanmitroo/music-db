from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


app_name = 'music'

urlpatterns = [
    # /music/
    url(r'^$', views.IndexView.as_view(), name='index'),


	url(r'^register/$', views.UserFormView.as_view(), name='register'),

    # /music/71/
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),

	# /music/album/add/
	url(r'^album/add/$', views.AlbumCreate.as_view(), name="album-add"),

	# /music/album/2/
	url(r'^album/(?P<pk>[0-9]+)/$', views.AlbumUpdate.as_view(), name="album-update"),

	# /music/album/2/delete/
	url(r'^album/(?P<pk>[0-9]+)/delete/$', views.AlbumDelete.as_view(), name="album-delete"),

    # /music/<album_id>/favorite
    url(r'^(?P<album_id>[0-9]+)/favorite/$', views.album_favorite, name='album_favorite'),

	# /music/<album_id>/<song_id/favorite
    url(r'^(?P<album_id>[0-9]+)/(?P<song_id>[0-9]+)/favorite/$', views.song_favorite, name='song_favorite'),

	# /music/album/api
    url(r'^albums/api/$', views.AlbumList.as_view(), name='albums_api'),

	# /music/songs/api
	url(r'^songs/api/$', views.SongList.as_view(), name='songs_api')

]


urlpatterns = format_suffix_patterns(urlpatterns)
