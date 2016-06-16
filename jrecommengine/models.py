from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import models


User = settings.JRECOMMENGINE["USER_MODEL"]
Item = settings.JRECOMMENGINE["ITEM_MODEL"]


class Like(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+", verbose_name="User")
   item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="+", verbose_name="Item")

   def save(self, *args, **kwargs):
      super(Like, self).save(*args, **kwargs)

      try:
         Dislike.objects.get(user=self.user, item=self.item).delete()
      except ObjectDoesNotExist:
         pass


   def __str__(self):
      return "(User: " + str(self.user) + ", Item: " + str(self.item) + ")"


   class Meta:
      unique_together = ("user", "item")
      verbose_name = "Like"
      verbose_name_plural = "Likes"


class Dislike(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+", verbose_name="User")
   item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="+", verbose_name="Item")

   def save(self, *args, **kwargs):
      super(Dislike, self).save(*args, **kwargs)

      try:
         Like.objects.get(user=self.user, item=self.item).delete()
      except ObjectDoesNotExist:
         pass


   def __str__(self):
      return "(User: " + str(self.user) + ", Item: " + str(self.item) + ")"


   class Meta:
      unique_together = ("user", "item")
      verbose_name = "Dislike"
      verbose_name_plural = "Dislikes"


class Similarity(models.Model):
   user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+", verbose_name="User")
   user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+", verbose_name="User")
   index = models.FloatField(verbose_name="Index")

   def __str__(self):
      return "(User: " + str(self.user1) + ", User: " + str(self.user2) + ", Index: " + str(self.index) + ")"


   class Meta:
      unique_together = ("user1", "user2")
      verbose_name = "Similarity"
      verbose_name_plural = "Similarities"
      ordering = ("-index",)


class Suggestion(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+", verbose_name="User")
   item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="+", verbose_name="Item")
   weight = models.FloatField(verbose_name="Weight")

   def __str__(self):
      return "(User: " + str(self.user) + ", Item: " + str(self.item) + ", Weight: " + str(self.weight) + ")"


   class Meta:
      unique_together = ("user", "item")
      verbose_name = "Suggestion"
      verbose_name_plural = "Suggestions"
      ordering = ("-weight",)
