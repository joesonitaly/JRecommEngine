=============
JRecommEngine
=============

JRecommEngine is a collaborative-filtering recommendation engine.
It is based on the Jaccard similarity index.

Quick start
-----------

1. Add "jrecommengine" to your INSTALLED_APPS setting like this::

   INSTALLED_APPS = [
       ...
       'jrecommengine',
   ]

2. Also in your INSTALLED_APPS setting, set the User and Item models::

   JRECOMMENGINE = {
                      "USER_MODEL": "app.model",
                      "ITEM_MODEL": "app.model"
                   }

2. Run migrations to create the jrecommengine models.

3. If needed, random ratings can be generated using jrecommengine.random_ratings.setRandomRatings().
