#! /usr/bin/env python

fixtures = {
              "jrecommengine": [
                               ],
           }

from subprocess import call

call(["python", "manage.py", "makemigrations"])
call(["python", "manage.py", "migrate"])

if fixtures:
   print("\n***** Starting *****\n")

   if isinstance(fixtures, dict):
      for app in fixtures:
         if fixtures[app]:
            call(["python", "manage.py", "loaddata", "-v 1", "--app", app, "-i"] + list(fixtures[app]))
         else:
            from os import listdir
            call(["python", "manage.py", "loaddata", "-v 1", "--app", app, "-i"] + listdir(app + "/fixtures/"))
   else:
      call(["python", "manage.py", "loaddata", "-v 1", "-i"] + list(fixtures))

   print("\n***** Done *****")
