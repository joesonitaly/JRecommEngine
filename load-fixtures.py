#! /usr/bin/env python

from os import listdir
from subprocess import call
from sys import stdout


fixtures = {
              "jrecommengine": [
                               ],
           }

stdout.write("***** Starting *****\n\n")

call(["python", "manage.py", "makemigrations"])
call(["python", "manage.py", "migrate"])

if fixtures:
   if isinstance(fixtures, dict):
      for app in fixtures:
         if fixtures[app]:
            call(["python", "manage.py", "loaddata", "-v 1", "--app", app, "-i"] + list(fixtures[app]))
         else:
            call(["python", "manage.py", "loaddata", "-v 1", "--app", app, "-i"] + listdir(app + "/fixtures/"))
   else:
      call(["python", "manage.py", "loaddata", "-v 1", "-i"] + list(fixtures))

stdout.write("\n***** Done *****\n")
