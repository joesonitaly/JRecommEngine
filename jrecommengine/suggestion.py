import math

from django.core.exceptions import ObjectDoesNotExist

from .models import User, Movie, Suggestion as SuggestionModel


class Suggestion:
   def __init__(self, engine):
      self.engine = engine


   def suggestionsForUser(self, user):
      self.update(user)
      return [suggestion.movie for suggestion in SuggestionModel.objects.filter(user=user).all()]


   def update(self, user):
      try:
         user = User.objects.get(username=user.username)
      except ObjectDoesNotExist:
         return """ToDo: Add proper error handling."""

      userLikedMovies = self.engine.moviesLikedByUser(user)
      userDislikedMovies = self.engine.moviesDislikedByUser(user)
      userUnratedMovies = frozenset(Movie.objects.all()) - (frozenset(userLikedMovies) | frozenset(userDislikedMovies))

      similarUsers = self.engine.similarities.usersSimilarToUser(user)

      for movie in userUnratedMovies:
         indicesOfLikes = [similarUser[1] for similarUser in similarUsers if movie in self.engine.moviesLikedByUser(similarUser[0])]
         indicesOfDislikes = [similarUser[1] for similarUser in similarUsers if movie in self.engine.moviesDislikedByUser(similarUser[0])]

         if indicesOfLikes or indicesOfDislikes:
            weight = (math.fsum(indicesOfLikes) - math.fsum(indicesOfDislikes)) / (len(indicesOfLikes) + len(indicesOfDislikes))

            try:
               suggestion = SuggestionModel.objects.get(user=user, movie=movie)

               if suggestion.weight != weight:
                  suggestion.weight = weight
                  suggestion.save(update_fields=("weight",))
            except ObjectDoesNotExist:
               SuggestionModel.objects.create(user=user, movie=movie, weight=weight)
         else:
            try:
               SuggestionModel.objects.get(user=user, movie=movie).delete()
            except ObjectDoesNotExist:
               pass
