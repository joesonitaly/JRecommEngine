=============
JRecommEngine
=============

JRecommEngine is a collaborative-filtering recommendation engine.
It is based on the Jaccard similarity index.

Detailed documentation is in the 'docs' directory.

Quick start
-----------

1. Add "jrecommengine" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'jrecommengine',
    ]

2. Run `python manage.py migrate` to create the jrecommengine models.
   Alternatively, you can run the load-fixtures module to install the
   supplied sample data.
