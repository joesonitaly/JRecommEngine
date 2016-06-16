from random import seed, randint

from .config import *
from .engine import *
from .models import Like, Dislike, Similarity, Suggestion


def setRandomRatings():
   print("***** Starting *****\n")

   items = Item.objects.all()
   itemsLength = len(items)

   users = User.objects.all()

   engine = Engine()

   Like.objects.all().delete()
   Dislike.objects.all().delete()

   seed()

   for user in users:
      selectedItems = []

      for _ in range(0, randint(0, itemsLength)):
         item = items[randint(0, itemsLength - 1)]

         while item in selectedItems:
            item = items[randint(0, itemsLength - 1)]

         engine.likes.add(user=user, item=item)
         selectedItems.append(item)

         try:
            print("<Like: " + str(Like.objects.get(user=user, item=item)) + ">")
         except ObjectDoesNotExist:
            pass

      for _ in range(0, randint(0, itemsLength - len(selectedItems))):
         item = items[randint(0, itemsLength - 1)]

         while item in selectedItems:
            item = items[randint(0, itemsLength - 1)]

         engine.dislikes.add(user=user, item=item)
         selectedItems.append(item)

         try:
            print("<Dislike: " + str(Dislike.objects.get(user=user, item=item)) + ">")
         except ObjectDoesNotExist:
            pass

   Similarity.objects.all().delete()
   Suggestion.objects.all().delete()

   print("\n***** Done *****")
