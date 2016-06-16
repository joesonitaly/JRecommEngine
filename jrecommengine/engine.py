from math import fsum

from django.db.models import Q

from .config import *
from .models import Like, Dislike, Similarity, Suggestion
from .rating import *


class Engine:
   def __init__(self):
      self.likes = Rating(self, "like")
      self.dislikes = Rating(self, "dislike")


   def itemsLikedByUser(self, user):
      return [like.item for like in Like.objects.filter(user=user)]


   def itemsDislikedByUser(self, user):
      return [dislike.item for dislike in Dislike.objects.filter(user=user)]


   def usersWhoLikeItem(self, item):
      return [like.user for like in Like.objects.filter(item=item)]


   def usersWhoDislikeItem(self, item):
      return [dislike.user for dislike in Dislike.objects.filter(item=item)]


   def usersSimilarToUser(self, user):
      return [((similarity.user1 if (similarity.user2 == user) else similarity.user2), similarity.index) for similarity in Similarity.objects.filter(Q(user1=user) | Q(user2=user)).all()]


   def updateSimilaritiesForUser(self, user):
      userLikedItems = frozenset(self.itemsLikedByUser(user))
      userDislikedItems = frozenset(self.itemsDislikedByUser(user))

      otherUsers = User.objects.exclude(pk=user.pk).all()

      for otherUser in otherUsers:
         otherUserLikedItems = frozenset(self.itemsLikedByUser(otherUser))
         otherUserDislikedItems = frozenset(self.itemsDislikedByUser(otherUser))

         if not userLikedItems.isdisjoint(otherUserLikedItems) or not userDislikedItems.isdisjoint(otherUserDislikedItems):
            index = (len(userLikedItems & otherUserLikedItems) + len(userDislikedItems & otherUserDislikedItems) - len(userLikedItems & otherUserDislikedItems) - len(userDislikedItems & otherUserLikedItems)) / len(userLikedItems | otherUserLikedItems | userDislikedItems | otherUserDislikedItems)

            try:
               similarity = Similarity.objects.get((Q(user1=user) & Q(user2=otherUser)) | (Q(user1=otherUser) & Q(user2=user)))

               if similarity.index != index:
                  similarity.index = index
                  similarity.save(update_fields=("index",))
            except ObjectDoesNotExist:
               Similarity.objects.create(user1=user, user2=otherUser, index=index)
         else:
            try:
               Similarity.objects.get((Q(user1=user) & Q(user2=otherUser)) | (Q(user1=otherUser) & Q(user2=user))).delete()
            except ObjectDoesNotExist:
               pass


   def suggestionsForUser(self, user):
      self.updateSuggestionsForUser(user)
      return [suggestion.item for suggestion in Suggestion.objects.filter(user=user).all()]


   def updateSuggestionsForUser(self, user):
      userLikedItems = self.itemsLikedByUser(user)
      userDislikedItems = self.itemsDislikedByUser(user)

      userUnratedItems = frozenset(Item.objects.all()) - (frozenset(userLikedItems) | frozenset(userDislikedItems))
      similarUsers = self.usersSimilarToUser(user)

      for item in userUnratedItems:
         indicesOfLikes = [similarUser[1] for similarUser in similarUsers if item in self.itemsLikedByUser(similarUser[0])]
         indicesOfDislikes = [similarUser[1] for similarUser in similarUsers if item in self.itemsDislikedByUser(similarUser[0])]

         if indicesOfLikes or indicesOfDislikes:
            weight = (fsum(indicesOfLikes) - fsum(indicesOfDislikes)) / (len(indicesOfLikes) + len(indicesOfDislikes))

            try:
               suggestion = Suggestion.objects.get(user=user, item=item)

               if suggestion.weight != weight:
                  suggestion.weight = weight
                  suggestion.save(update_fields=("weight",))
            except ObjectDoesNotExist:
               Suggestion.objects.create(user=user, item=item, weight=weight)
         else:
            try:
               Suggestion.objects.get(user=user, item=item).delete()
            except ObjectDoesNotExist:
               pass
