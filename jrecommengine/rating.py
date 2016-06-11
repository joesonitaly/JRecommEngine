from django.core.exceptions import ObjectDoesNotExist

from .models import User, Movie, Like, Dislike


class Rating:
   def __init__(self, engine, kind):
      self.engine = engine
      self.kind = kind


   def add(self, user, movie):
      try:
         user = User.objects.get(username=user.username)
         movie = Movie.objects.get(title=movie.title, year=movie.year)
      except ObjectDoesNotExist:
         return """ToDo: Add proper error handling."""

      if self.kind == "like":
         Like.objects.create(user=user, movie=movie)
      else:
         Dislike.objects.create(user=user, movie=movie)


   def remove(self, user, movie):
      try:
         user = User.objects.get(username=user.username)
         movie = Movie.objects.get(title=movie.title, year=movie.year)
      except ObjectDoesNotExist:
         return """ToDo: Add proper error handling."""

      if self.kind == "like":
         Like.objects.get(user=user, movie=movie).delete()
      else:
         Dislike.objects.get(user=user, movie=movie).delete()
