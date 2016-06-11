from .models import Like, Dislike
from .rating import Rating
from .similarity import Similarity
from .suggestion import Suggestion


class Engine:
   def __init__(self):
      self.likes = Rating(self, "like")
      self.dislikes = Rating(self, "dislike")
      self.similarities = Similarity(self)
      self.suggestions = Suggestion(self)


   def moviesLikedByUser(self, user):
      return [like.movie for like in Like.objects.filter(user=user)]


   def moviesDislikedByUser(self, user):
      return [dislike.movie for dislike in Dislike.objects.filter(user=user)]


   def usersWhoLikeMovie(self, movie):
      return [like.user for like in Like.objects.filter(movie=movie)]


   def usersWhoDislikeMovie(self, movie):
      return [dislike.user for dislike in Dislike.objects.filter(movie=movie)]
