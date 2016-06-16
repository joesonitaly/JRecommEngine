from django.apps import apps
from django.conf import settings


User = apps.get_model(settings.JRECOMMENGINE["USER_MODEL"])
Item = apps.get_model(settings.JRECOMMENGINE["ITEM_MODEL"])
