To get running:

copy Androkon/androkon/androkon/settings.py.template to just settings.py, and edit lines 15 and 109, to change db file and template folder locations respectively.
Point the template folder at Androkon/templates, and the db file whereever you want, it'll be created there.

cd to Androkon/androkon and run python manage.py syncdb to create the database.

run python manage.py runserver to start server, then point browser at localhost:8000 to view

If you are ian: change SECRET_KEY on line 81 of settings.py, otherwise it doesn't matter for just testing
