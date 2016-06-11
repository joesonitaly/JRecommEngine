from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from .models import User, Similarity as SimilarityModel


class Similarity:
   def __init__(self, engine):
      self.engine = engine


   def usersSimilarToUser(self, user):
      self.update(user)
      return [((similarity.user1 if (similarity.user2 == user) else similarity.user2), similarity.index) for similarity in SimilarityModel.objects.filter(Q(user1=user) | Q(user2=user)).all()]


   def update(self, user):
      try:
         user = User.objects.get(username=user.username)
      except ObjectDoesNotExist:
         return """ToDo: Add proper error handling."""

      userLikedMovies = frozenset(self.engine.moviesLikedByUser(user))
      userDislikedMovies = frozenset(self.engine.moviesDislikedByUser(user))

      otherUsers = User.objects.exclude(username=user.username).all()

      for otherUser in otherUsers:
         otherUserLikedMovies = frozenset(self.engine.moviesLikedByUser(otherUser))
         otherUserDislikedMovies = frozenset(self.engine.moviesDislikedByUser(otherUser))

         if not userLikedMovies.isdisjoint(otherUserLikedMovies) or not userDislikedMovies.isdisjoint(otherUserDislikedMovies):
            index = (len(userLikedMovies & otherUserLikedMovies) + len(userDislikedMovies & otherUserDislikedMovies) - len(userLikedMovies & otherUserDislikedMovies) - len(userDislikedMovies & otherUserLikedMovies)) / len(userLikedMovies | otherUserLikedMovies | userDislikedMovies | otherUserDislikedMovies)

            try:
               similarity = SimilarityModel.objects.get((Q(user1=user) & Q(user2=otherUser)) | (Q(user1=otherUser) & Q(user2=user)))

               if similarity.index != index:
                  similarity.index = index
                  similarity.save(update_fields=("index",))
            except ObjectDoesNotExist:
               SimilarityModel.objects.create(user1=user, user2=otherUser, index=index)
         else:
            try:
               SimilarityModel.objects.get((Q(user1=user) & Q(user2=otherUser)) | (Q(user1=otherUser) & Q(user2=user))).delete()
            except ObjectDoesNotExist:
               pass
