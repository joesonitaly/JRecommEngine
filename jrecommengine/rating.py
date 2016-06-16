from django.core.exceptions import ObjectDoesNotExist

from .models import Like, Dislike


class Rating:
   def __init__(self, engine, kind):
      self.engine = engine
      self.kind = kind


   def add(self, user, item):
      if self.kind == "like":
         Like.objects.create(user=user, item=item)
      else:
         Dislike.objects.create(user=user, item=item)

      self.engine.updateSimilaritiesForUser(user)


   def remove(self, user, item):
      try:
         if self.kind == "like":
            Like.objects.get(user=user, item=item).delete()
         else:
            Dislike.objects.get(user=user, item=item).delete()

         self.engine.updateSimilaritiesForUser(user)
      except ObjectDoesNotExist:
         pass
