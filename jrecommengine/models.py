from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Q


class User(models.Model):
   username = models.CharField(max_length=255, verbose_name="Username", unique=True)

   def __str__(self):
      return self.username


   class Meta:
      verbose_name = "User"
      verbose_name_plural = "Users"


class Movie(models.Model):
   title = models.CharField(max_length=255, verbose_name="Title")
   year = models.PositiveSmallIntegerField(verbose_name="Year")

   def __str__(self):
      return self.title


   class Meta:
      unique_together = ("title", "year")
      verbose_name = "Movie"
      verbose_name_plural = "Movies"


class Like(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+", verbose_name="User")
   movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="+", verbose_name="Movie")

   def save(self, *args, **kwargs):
      try:
         Like.objects.get(user=self.user, movie=self.movie)
         return
      except ObjectDoesNotExist:
         super(Like, self).save(*args, **kwargs)

         try:
            Dislike.objects.get(user=self.user, movie=self.movie).delete()
         except ObjectDoesNotExist:
            pass


   def __str__(self):
      return "(User: " + str(self.user) + ", Movie: " + str(self.movie) + ")"


   class Meta:
      unique_together = ("user", "movie")
      verbose_name = "Like"
      verbose_name_plural = "Likes"


class Dislike(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+", verbose_name="User")
   movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="+", verbose_name="Movie")

   def save(self, *args, **kwargs):
      try:
         Dislike.objects.get(user=self.user, movie=self.movie)
         return
      except ObjectDoesNotExist:
         super(Dislike, self).save(*args, **kwargs)

         try:
            Like.objects.get(user=self.user, movie=self.movie).delete()
         except ObjectDoesNotExist:
            pass


   def __str__(self):
      return "(User: " + str(self.user) + ", Movie: " + str(self.movie) + ")"


   class Meta:
      unique_together = ("user", "movie")
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
   movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="+", verbose_name="Movie")
   weight = models.FloatField(verbose_name="Weight")

   def __str__(self):
      return "(User: " + str(self.user) + ", Movie: " + str(self.movie) + ", Weight: " + str(self.weight) + ")"


   class Meta:
      unique_together = ("user", "movie")
      verbose_name = "Suggestion"
      verbose_name_plural = "Suggestions"
      ordering = ("-weight",)
