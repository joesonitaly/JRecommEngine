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

def setRandomRatings():
   from random import randint

   from .engine import Engine
   from .models import Similarity, Suggestion

   print("***** Starting *****\n")

   movies = Movie.objects.all()
   moviesLength = len(movies)

   users = User.objects.all()

   engine = Engine()

   Like.objects.all().delete()
   Dislike.objects.all().delete()

   Similarity.objects.all().delete()
   Suggestion.objects.all().delete()

   for user in users:
      selectedMovies = []

      for _ in range(0, randint(0, moviesLength)):
         movie = movies[randint(0, moviesLength - 1)]

         while movie in selectedMovies:
            movie = movies[randint(0, moviesLength - 1)]

         engine.likes.add(user=user, movie=movie)
         selectedMovies.append(movie)

         try:
            print("<Like: " + str(Like.objects.get(user=user, movie=movie)) + ">")
         except ObjectDoesNotExist:
            pass

      for _ in range(0, randint(0, moviesLength - len(selectedMovies))):
         movie = movies[randint(0, moviesLength - 1)]

         while movie in selectedMovies:
            movie = movies[randint(0, moviesLength - 1)]

         engine.dislikes.add(user=user, movie=movie)
         selectedMovies.append(movie)

         try:
            print("<Dislike: " + str(Dislike.objects.get(user=user, movie=movie)) + ">")
         except ObjectDoesNotExist:
            pass

   print("\n***** Done *****")
