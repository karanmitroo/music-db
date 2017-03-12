from rest_framework import serializers

from .models import Album, Song

class AlbumSerializer(serializers.ModelSerializer):

	class Meta:
		model = Album
		fields = ('id','artist', 'album_title', 'genre', 'album_logo')


class SongSerializer(serializers.ModelSerializer):
	album = AlbumSerializer()

	class Meta:
		model = Song
		fields = ('album', 'song_title')
