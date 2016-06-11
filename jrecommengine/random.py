import random
import sys

from django.core.exceptions import ObjectDoesNotExist

from .engine import Engine
from .models import User, Movie, Like, Dislike, Similarity, Suggestion


def setRandomRatings():
   sys.stdout.write("***** Starting *****\n\n")

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

      for _ in range(0, random.randint(0, moviesLength)):
         movie = movies[random.randint(0, moviesLength - 1)]

         while movie in selectedMovies:
            movie = movies[random.randint(0, moviesLength - 1)]

         engine.likes.add(user=user, movie=movie)
         selectedMovies.append(movie)

         try:
            print("<Like: " + str(Like.objects.get(user=user, movie=movie)) + ">")
         except ObjectDoesNotExist:
            pass

      for _ in range(0, random.randint(0, moviesLength - len(selectedMovies))):
         movie = movies[random.randint(0, moviesLength - 1)]

         while movie in selectedMovies:
            movie = movies[random.randint(0, moviesLength - 1)]

         engine.dislikes.add(user=user, movie=movie)
         selectedMovies.append(movie)

         try:
            print("<Dislike: " + str(Dislike.objects.get(user=user, movie=movie)) + ">")
         except ObjectDoesNotExist:
            pass

   sys.stdout.write("\n***** Done *****\n")
